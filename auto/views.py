from django.shortcuts import render, redirect
from .forms import *
from main.models import *
from django.contrib import messages
from datetime import datetime
from manual.extras import *
from .backtracking import *
from .extras import *
from .map import *
from .map import twyc_map
from users.decorators import *
from users.decorators import unauthenticated_user, allowed_users
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
#@valid_date
def automatic(request):

    student = request.user.student
    date = EveningDate.objects.get(year_group=student.year_group)
    timeslots =  date.timeslots.all()
    timeslots = sortTimeslots(timeslots)

    if request.method == 'POST':
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        if start_time >= end_time:
            messages.info(request, 'Invalid Input')
        else:

            # Find all timeslots in the ranage given excluding timeslots already booked by student

            userTimeslots = []
            for timeslot in timeslots:
                if str(timeslot) >= start_time and str(timeslot) <= end_time:

                    bookings = request.user.student.booking_set.all()
                    timeslotsBooked = []
                    for booking in bookings:
                        timeslotsBooked.append(booking.timeslot)

                    if timeslot not in timeslotsBooked:
                        userTimeslots.append(timeslot)



            # Number of how many teachers are left
            teachersLeft = student.teachers.all().count() - request.user.student.booking_set.all().count()

            # Get list of teachers that havent been booked with
            teachersBooked = []
            teachers = []

            for booking in request.user.student.booking_set.all():
                teachersBooked.append(booking.teacher)
            
            for teacher in student.teachers.all():
                if teacher not in teachersBooked:
                    teachers.append(teacher)








            if teachersLeft == len(userTimeslots):

                # Get list of teachers availabiltity

                teachersAv = []
                teachersAv = teachersAvailabilityAuto(teachers, userTimeslots, date)

                # Backtrack once to get possible solutions

                result = teacherBacktracking(teachersAv, userTimeslots)


                # Add those solutions to a queue


                solutionQueue = DynamicQueue()

                for solution in result:
                    solutionDict = {}

                    # For all timeslots on day either unavaiable or teacher

                    # {'16:00':'Mrs.Lever'}

                    for i in range(0, len(userTimeslots)):
                        solutionDict[userTimeslots[i]] = solution[i]

                    # Add all available timeslots with 0

                    for timeslot in timeslots:
                        if timeslot not in userTimeslots:
                            solutionDict[timeslot] = 0

                    # Update all timeslots with booked teacher

                    for booking in request.user.student.booking_set.all():
                        solutionDict[booking.timeslot] = booking.teacher.name
                    

                    solutionQueue.enQueue(solutionDict)

                    if solutionQueue.isFull():
                        break
                

                if solutionQueue.getQueueLength() != 0:

                    finalSolutions = []

                    while solutionQueue.isEmpty() == False:

                        currentDict = solutionQueue.deQueue()

                        # Get start and end timeslot


                        startFound = False
                        index = 0

                        while not startFound:
                            if currentDict[timeslots[index]] == 0:
                                del currentDict[timeslots[index]]
                                index += 1
                            else:
                                startFound = True
                        

                        endFound = False
                        index = len(timeslots) - 1

                        while not endFound:
                            if currentDict[timeslots[index]] == 0:
                                del currentDict[timeslots[index]]
                                index -= 1
                            else:
                                endFound = True


                        # Calculate Breaks and Distance                           

                        distance = 0
                        breaks = 0
                        teachersOrder = []

                        # Calculate number of breaks between start and end appointments

                        for timeslot in timeslots:
                            if timeslot in currentDict.keys():
                                if currentDict[timeslot] == 0:
                                    breaks += 1
                                else:
                                    teachersOrder.append(currentDict[timeslot])


                        # Put through graph
                        

                        count = 0

                        while count < len(teachersOrder)-1:

                            currentTeacher = Teacher.objects.get(name=teachersOrder[count])
                            nextTeacher = Teacher.objects.get(name=teachersOrder[count+1])

                            map = twyc_map
                            currentNode = map.getNode(currentTeacher.building.name)

                            if currentTeacher.building != nextTeacher.building:
                                nodeWeight = currentNode.getLinkWeight(nextTeacher.building.name)
                            else:
                                nodeWeight = 0

                            distance += nodeWeight
                            count += 1

                        currentDict['Breaks'] = breaks
                        currentDict['Distance'] = distance

                        finalSolutions.append(currentDict)


                    # Sort solutions on breaks or distance


                    finalSolutions = bubbleSortBreaks(finalSolutions)

                    
                    # Put solutions in stack get pop (best solution)
                    

                    solutionStack = Stack(finalSolutions)

                    optimalSolutions = []

                    if solutionStack.getStackLength() > 1:

                        optimalBreakSolution = solutionStack.pop()
                        optimalSolutions.append(optimalBreakSolution)
                        optimalBreakSolution = solutionStack.pop()


                        while optimalBreakSolution['Breaks'] == optimalSolutions[0]['Breaks']:
                            optimalSolutions.append(optimalBreakSolution)

                            if solutionStack.getStackLength() == 0:
                                break
                            else:
                                optimalBreakSolution = solutionStack.pop()



                        if len(optimalSolutions) > 1:
                            optimalSolutions = bubbleSortDistance(optimalSolutions)
                            optimalBreakSolution = optimalSolutions[0]
                        else:
                            optimalBreakSolution = optimalSolutions[0]

                    else:
                        optimalBreakSolution = solutionStack.pop()


                    # Remove curremt bookings and empty bookings


                    for booking in request.user.student.booking_set.all():
                        del optimalBreakSolution[booking.timeslot]
                    
                    for timeslot in timeslots:
                        if timeslot in optimalBreakSolution.keys():
                            if optimalBreakSolution[timeslot] == 0:
                                del optimalBreakSolution[timeslot]
                    

                    # Book appointments

                    for timeslot in timeslots:
                        if timeslot in optimalBreakSolution.keys():
                            if Booking.objects.filter(teacher=Teacher.objects.get(name=optimalBreakSolution[timeslot]), timeslot=timeslot, date=date).count() == 0:
                                Booking.objects.create(
                                    student=student,
                                    teacher=Teacher.objects.get(name=optimalBreakSolution[timeslot]),
                                    timeslot=timeslot,
                                    status='Pending',
                                    date=date,
                                )
                    
                    return redirect('userStudentBookings')
                
                else:
                    messages.info(request, 'There are no solutions')

                

                
                











            elif teachersLeft < len(userTimeslots):

                # Get all timeslot patterns
                res = timeslotBacktracking(userTimeslots)
                timeslotPatterns = []
                for record in res:
                    if len(record) == teachersLeft:
                        timeslotPatterns.append(record)


                newTimeslotPatterns = []

                for index in range(len(timeslotPatterns)-1,-1,-1):
                    newTimeslotPatterns.append(timeslotPatterns[index])


                solutionQueue = DynamicQueue()


                for timeslotPattern in newTimeslotPatterns:


                    # Get list of teachers availabiltity

                    teachersAv = []
                    teachersAv = teachersAvailabilityAuto(teachers, timeslotPattern, date)


                    # Backtrack once to get possible solutions

                    result = teacherBacktracking(teachersAv, timeslotPattern)


                    # Add those solutions to a queue

                    
                    for solution in result:
                        solutionDict = {}

                        # For all timeslots on day either unavaiable or teacher

                        # {'16:00':'Mrs.Lever'}

                        for i in range(0, len(timeslotPattern)):
                            solutionDict[timeslotPattern[i]] = solution[i]

                        # Add all available timeslots with 0

                        for timeslot in timeslots:
                            if timeslot not in timeslotPattern:
                                solutionDict[timeslot] = 0

                        # Update all timeslots with booked teacher

                        for booking in request.user.student.booking_set.all():
                            solutionDict[booking.timeslot] = booking.teacher.name


                        solutionQueue.enQueue(solutionDict)

                        if solutionQueue.isFull():
                            break

                    if solutionQueue.isFull():
                            break


                

                if solutionQueue.getQueueLength() != 0:



                    finalSolutions = []

                    while solutionQueue.isEmpty() == False:

                        currentDict = solutionQueue.deQueue()

                        # Get start and end timeslot


                        startFound = False
                        index = 0

                        while not startFound:
                            if currentDict[timeslots[index]] == 0:
                                del currentDict[timeslots[index]]
                                index += 1
                            else:
                                startFound = True
                        

                        endFound = False
                        index = len(timeslots) - 1

                        while not endFound:
                            if currentDict[timeslots[index]] == 0:
                                del currentDict[timeslots[index]]
                                index -= 1
                            else:
                                endFound = True


                        # Calculate breaks and distance                           

                        distance = 0
                        breaks = 0
                        teachersOrder = []

                        # Calculate breaks between start and end appointments

                        for timeslot in timeslots:
                            if timeslot in currentDict.keys():
                                if currentDict[timeslot] == 0:
                                    breaks += 1
                                else:
                                    teachersOrder.append(currentDict[timeslot])

                        # Put through graph 
                        

                        count = 0

                        while count < len(teachersOrder)-1:

                            currentTeacher = Teacher.objects.get(name=teachersOrder[count])
                            nextTeacher = Teacher.objects.get(name=teachersOrder[count+1])

                            map = twyc_map
                            currentNode = map.getNode(currentTeacher.building.name)

                            if currentTeacher.building != nextTeacher.building:
                                nodeWeight = currentNode.getLinkWeight(nextTeacher.building.name)
                            else:
                                nodeWeight = 0

                            distance += nodeWeight
                            count += 1

                        currentDict['Breaks'] = breaks
                        currentDict['Distance'] = distance

                        finalSolutions.append(currentDict)



                    # Sort solutions on breaks or distance
                    

                    finalSolutions = bubbleSortBreaks(finalSolutions)


                    # Put solutions in a stack

                    solutionStack = Stack(finalSolutions)
                    optimalSolutions = []

                    if solutionStack.getStackLength() > 1:

                        optimalBreakSolution = solutionStack.pop()
                        optimalSolutions.append(optimalBreakSolution)
                        optimalBreakSolution = solutionStack.pop()


                        while optimalBreakSolution['Breaks'] == optimalSolutions[0]['Breaks']:
                            optimalSolutions.append(optimalBreakSolution)

                            if solutionStack.getStackLength() == 0:
                                break
                            else:
                                optimalBreakSolution = solutionStack.pop()



                        if len(optimalSolutions) > 1:
                            optimalSolutions = bubbleSortDistance(optimalSolutions)
                            optimalBreakSolution = optimalSolutions[0]
                        else:
                            optimalBreakSolution = optimalSolutions[0]

                    else:
                        optimalBreakSolution = solutionStack.pop()




                    # Remove current bookings and empty bookings

                    for booking in request.user.student.booking_set.all():
                        del optimalBreakSolution[booking.timeslot]
                    
                    for timeslot in timeslots:
                        if timeslot in optimalBreakSolution.keys():
                            if optimalBreakSolution[timeslot] == 0:
                                del optimalBreakSolution[timeslot]


                    # Book appointments

                    for timeslot in timeslots:
                        if timeslot in optimalBreakSolution.keys():
                            if Booking.objects.filter(teacher=Teacher.objects.get(name=optimalBreakSolution[timeslot]), timeslot=timeslot, date=date).count() == 0:
                                Booking.objects.create(
                                    student=student,
                                    teacher=Teacher.objects.get(name=optimalBreakSolution[timeslot]),
                                    timeslot=timeslot,
                                    status='Pending',
                                    date=date,
                                )

                    
                    return redirect('userStudentBookings')
                
                else:
                    messages.info(request, 'There are no solutions')

                









            elif teachersLeft > len(userTimeslots):
                messages.info(request, 'Time range to small to book for all teachers')

            



    

    context = {'timeslots':timeslots}
    return render(request, 'auto/auto.html', context)
