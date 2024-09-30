from django.shortcuts import render, redirect
from .forms import *
from main.models import *
from django.contrib.auth.decorators import login_required
from users.decorators import unauthenticated_user, allowed_users
from django.contrib import messages

# Create your views here.

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteAll(request):

    uvi_students = Student.objects.filter(year_group="UVI")

    if request.method == "POST":
        for student in uvi_students:
            student.delete()
        return redirect('dashboard')


    context = {}
    return render(request, 'crud/delete_all_UVI.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def convertAll(request):

    lvi_students = Student.objects.filter(year_group="LVI")

    if request.method == "POST":
        for student in lvi_students:
            student.year_group = "UVI"
            student.save()

        return redirect('dashboard')


    context = {}
    return render(request, 'crud/convert_all_LVI.html', context)








# CRUD for parents

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createParent(request):

    form = ParentForm()

    if request.method == 'POST':
        #print(request.POST)

        form = ParentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')


    context = {'form':form}
    return render(request, 'crud/create_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def editParent(request, pk):

    parent = Parent.objects.get(id=pk)

    form = ParentForm(instance=parent)

    if request.method == 'POST':
        #print(request.POST)

        form = ParentForm(request.POST, instance=parent)
        if form.is_valid():
            form.save()
            return redirect('dashboard')


    context = {'form':form}
    return render(request, 'crud/create_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteParent(request, pk):

    parent = Parent.objects.get(id=pk)

    if request.method == "POST":
        parent.delete()
        return redirect('dashboard')


    context = {'item':parent}
    return render(request, 'crud/delete.html', context)






# CRUD for Buildings

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createBuilding(request):

    form = BuildingForm()

    if request.method == 'POST':
        #print(request.POST)

        form = BuildingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')


    context = {'form':form}
    return render(request, 'crud/create_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def editBuilding(request, pk):

    building = Building.objects.get(id=pk)

    form = BuildingForm(instance=building)

    if request.method == 'POST':
        #print(request.POST)

        form = BuildingForm(request.POST, instance=building)
        if form.is_valid():
            form.save()
            return redirect('dashboard')


    context = {'form':form}
    return render(request, 'crud/create_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteBuilding(request, pk):

    building = Building.objects.get(id=pk)

    if request.method == "POST":
        building.delete()
        return redirect('dashboard')


    context = {'item':building}
    return render(request, 'crud/delete.html', context)








# CRUD for Rooms

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createRoom(request):

    form = RoomForm()

    if request.method == 'POST':
        #print(request.POST)

        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')


    context = {'form':form}
    return render(request, 'crud/create_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def editRoom(request, pk):

    room = Room.objects.get(id=pk)

    form = RoomForm(instance=room)

    if request.method == 'POST':
        #print(request.POST)

        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('dashboard')


    context = {'form':form}
    return render(request, 'crud/create_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteRoom(request, pk):

    room = Room.objects.get(id=pk)

    if request.method == "POST":
        room.delete()
        return redirect('dashboard')


    context = {'item':room}
    return render(request, 'crud/delete.html', context)








# CRUD for Subjects

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createSubject(request):

    form = SubjectForm()

    if request.method == 'POST':
        #print(request.POST)

        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')


    context = {'form':form}
    return render(request, 'crud/create_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def editSubject(request, pk):

    subject = Subject.objects.get(id=pk)

    form = SubjectForm(instance=subject)

    if request.method == 'POST':
        #print(request.POST)

        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            return redirect('dashboard')


    context = {'form':form}
    return render(request, 'crud/create_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteSubject(request, pk):

    subject = Subject.objects.get(id=pk)

    if request.method == "POST":
        subject.delete()
        return redirect('dashboard')


    context = {'item':subject}
    return render(request, 'crud/delete.html', context)









# CRUD for Timeslots

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createTimeslot(request):

    form = TimeslotForm()

    if request.method == 'POST':
        #print(request.POST)

        form = TimeslotForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')


    context = {'form':form}
    return render(request, 'crud/timeslot_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def editTimeslot(request, pk):

    timeslot = Timeslot.objects.get(id=pk)

    form = TimeslotForm(instance=timeslot)

    if request.method == 'POST':
        #print(request.POST)

        form = TimeslotForm(request.POST, instance=timeslot)
        if form.is_valid():
            form.save()
            return redirect('dashboard')


    context = {'form':form}
    return render(request, 'crud/timeslot_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteTimeslot(request, pk):

    timeslot = Timeslot.objects.get(id=pk)

    if request.method == "POST":
        timeslot.delete()
        return redirect('dashboard')


    context = {'item':timeslot}
    return render(request, 'crud/delete.html', context)








# CRUD for EveningDates

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createEveningDate(request):

    form = EveningDateForm()

    if request.method == 'POST':
        #print(request.POST)

        form = EveningDateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')


    context = {'form':form}
    return render(request, 'crud/date_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def editEveningDate(request, pk):

    eveningDate = EveningDate.objects.get(id=pk)

    form = EveningDateForm(instance=eveningDate)

    if request.method == 'POST':
        #print(request.POST)

        form = EveningDateForm(request.POST, instance=eveningDate)
        if form.is_valid():
            form.save()
            return redirect('dashboard')


    context = {'form':form}
    return render(request, 'crud/date_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteEveningDate(request, pk):

    eveningDate = EveningDate.objects.get(id=pk)

    if request.method == "POST":
        eveningDate.delete()
        return redirect('dashboard')


    context = {'item':eveningDate}
    return render(request, 'crud/delete.html', context)









# CRUD for Teachers

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createTeacher(request):

    form = TeacherForm()

    if request.method == 'POST':
        #print(request.POST)

        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')


    context = {'form':form}
    return render(request, 'crud/create_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def editTeacher(request, pk):

    teacher = Teacher.objects.get(id=pk)

    form = TeacherForm(instance=teacher)

    if request.method == 'POST':
        #print(request.POST)

        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect('dashboard')


    context = {'form':form}
    return render(request, 'crud/create_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteTeacher(request, pk):

    teacher = Teacher.objects.get(id=pk)

    if request.method == "POST":
        teacher.delete()
        return redirect('dashboard')


    context = {'item':teacher}
    return render(request, 'crud/delete.html', context)










# CRUD for Students

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createStudent(request):

    form = StudentForm()

    if request.method == 'POST':
        #print(request.POST)

        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')


    context = {'form':form}
    return render(request, 'crud/create_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def editStudent(request, pk):

    student = Student.objects.get(id=pk)

    form = StudentForm(instance=student)

    if request.method == 'POST':
        #print(request.POST)

        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('dashboard')


    context = {'form':form}
    return render(request, 'crud/create_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteStudent(request, pk):

    student = Student.objects.get(id=pk)

    if request.method == "POST":
        student.delete()
        return redirect('dashboard')


    context = {'item':student}
    return render(request, 'crud/delete.html', context)










# CRUD for Bookings

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def adminCreateBooking(request):

    form = BookingForm()

    if request.method == 'POST':
        form = BookingForm(request.POST)

        if form.is_valid():

            student = form.cleaned_data.get('student')
            teacher = form.cleaned_data.get('teacher')
            timeslot = form.cleaned_data.get('timeslot')
            date = form.cleaned_data.get('date')


            if student.year_group == date.year_group:

                if teacher in student.teachers.all():

                    if timeslot in date.timeslots.all():

                        if Booking.objects.filter(student=student, timeslot=timeslot, date=date).count() == 0:

                            if Booking.objects.filter(teacher=teacher, timeslot=timeslot, date=date).count() == 0:

                                if Booking.objects.filter(teacher=teacher, student=student, date=date).count() == 0:

                                    form.save()
                                    return redirect('bookings')
                                
                                else:
                                    messages.info(request, 'That student already has a booking with that teacher')

                            else:
                                messages.info(request, 'That teacher already has a booking at that time')
                        
                        else:
                            messages.info(request, 'That student already has a booking at that time')

                    else:
                        messages.info(request, 'That timeslot does not exist on that date')

                else:
                    messages.info(request, 'That student does not have that teacher')

            else:
                messages.info(request, 'That student cannot have a booking on that day')

    

    context = {'form':form}
    return render(request, 'crud/booking_form.html', context)






@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def adminEditBooking(request, pk):

    booking = Booking.objects.get(booking_id=pk)
    oldstudent = booking.student
    oldteacher = booking.teacher
    oldtimeslot = booking.timeslot

    form = BookingForm(instance=booking)
    

    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)

        if form.is_valid():

            student = form.cleaned_data.get('student')
            teacher = form.cleaned_data.get('teacher')
            timeslot = form.cleaned_data.get('timeslot')
            date = form.cleaned_data.get('date')


            if student.year_group == date.year_group:

                if teacher in student.teachers.all():

                    if timeslot in date.timeslots.all():




                        if student == oldstudent:

                            if teacher == oldteacher:
                                if Booking.objects.filter(student=student, timeslot=timeslot, date=date).count() == 0:

                                    if Booking.objects.filter(teacher=teacher, timeslot=timeslot, date=date).count() == 0:

                                        form.save()
                                        return redirect('bookings')
                                        
                                    else:
                                        messages.info(request, 'That teacher already has a booking at that time')

                                else:
                                    messages.info(request, 'That student already has a booking at that time')
                                    



                            elif timeslot == oldtimeslot:
                                if Booking.objects.filter(teacher=teacher, timeslot=timeslot, date=date).count() == 0:

                                    if Booking.objects.filter(teacher=teacher, student=student, date=date).count() == 0:

                                        form.save()
                                        return redirect('bookings')
                                        
                                    else:
                                        messages.info(request, 'That student already has a booking with that teacher')
                                        

                                else:
                                    messages.info(request, 'That teacher already has a booking at that time')
                                    
                            
                            else:

                                if Booking.objects.filter(student=student, timeslot=timeslot, date=date).count() == 0:

                                    if Booking.objects.filter(teacher=teacher, timeslot=timeslot, date=date).count() == 0:

                                        if Booking.objects.filter(teacher=teacher, student=student, date=date).count() == 0:

                                            form.save()
                                            return redirect('bookings')
                                        
                                        else:
                                            messages.info(request, 'That student already has a booking with that teacher')

                                    else:
                                        messages.info(request, 'That teacher already has a booking at that time')
                                
                                else:
                                    messages.info(request, 'That student already has a booking at that time')


                                
                        elif teacher == oldteacher:

                            if student == oldstudent:

                                if Booking.objects.filter(student=student, timeslot=timeslot, date=date).count() == 0:

                                    if Booking.objects.filter(teacher=teacher, timeslot=timeslot, date=date).count() == 0:

                                        form.save()
                                        return redirect('bookings')
                                        
                                    else:
                                        messages.info(request, 'That teacher already has a booking at that time')

                                else:
                                    messages.info(request, 'That student already has a booking at that time')
                                    



                            elif timeslot == oldtimeslot:

                                if Booking.objects.filter(student=student, timeslot=timeslot, date=date).count() == 0:

                                    if Booking.objects.filter(teacher=teacher, student=student, date=date).count() == 0:

                                        form.save()
                                        return redirect('bookings')
                                        
                                    else:
                                        messages.info(request, 'That student already has a booking with that teacher')
                                        

                                else:
                                    messages.info(request, 'That student already has a booking at that time')
                                    
                            
                            else:

                                if Booking.objects.filter(student=student, timeslot=timeslot, date=date).count() == 0:

                                    if Booking.objects.filter(teacher=teacher, timeslot=timeslot, date=date).count() == 0:

                                        if Booking.objects.filter(teacher=teacher, student=student, date=date).count() == 0:

                                            form.save()
                                            return redirect('bookings')
                                        
                                        else:
                                            messages.info(request, 'That student already has a booking with that teacher')

                                    else:
                                        messages.info(request, 'That teacher already has a booking at that time')
                                
                                else:
                                    messages.info(request, 'That student already has a booking at that time')


                        elif timeslot == oldtimeslot:

                            if student == oldstudent:

                                if Booking.objects.filter(teacher=teacher, timeslot=timeslot, date=date).count() == 0:

                                    if Booking.objects.filter(teacher=teacher, student=student, date=date).count() == 0:

                                        form.save()
                                        return redirect('bookings')
                                        
                                    else:
                                        messages.info(request, 'That student already has a booking with that teacher')

                                else:
                                    messages.info(request, 'That teacher already has a booking at that time')
                                    



                            elif teacher == oldteacher:

                                if Booking.objects.filter(student=student, timeslot=timeslot, date=date).count() == 0:

                                    if Booking.objects.filter(teacher=teacher, student=student, date=date).count() == 0:

                                        form.save()
                                        return redirect('bookings')
                                        
                                    else:
                                        messages.info(request, 'That student already has a booking with that teacher')
                                        

                                else:
                                    messages.info(request, 'That student already has a booking at that time')
                                    
                            
                            else:

                                if Booking.objects.filter(student=student, timeslot=timeslot, date=date).count() == 0:

                                    if Booking.objects.filter(teacher=teacher, timeslot=timeslot, date=date).count() == 0:

                                        if Booking.objects.filter(teacher=teacher, student=student, date=date).count() == 0:

                                            form.save()
                                            return redirect('bookings')
                                        
                                        else:
                                            messages.info(request, 'That student already has a booking with that teacher')

                                    else:
                                        messages.info(request, 'That teacher already has a booking at that time')
                                
                                else:
                                    messages.info(request, 'That student already has a booking at that time')


                        else:

                            if Booking.objects.filter(student=student, timeslot=timeslot, date=date).count() == 0:

                                if Booking.objects.filter(teacher=teacher, timeslot=timeslot, date=date).count() == 0:

                                    if Booking.objects.filter(teacher=teacher, student=student, date=date).count() == 0:

                                        form.save()
                                        return redirect('bookings')
                                        
                                    else:
                                        messages.info(request, 'That student already has a booking with that teacher')

                                else:
                                    messages.info(request, 'That teacher already has a booking at that time')
                                
                            else:
                                messages.info(request, 'That student already has a booking at that time')
                

                

                    else:
                        messages.info(request, 'That timeslot does not exist on that date')

                else:
                    messages.info(request, 'That student does not have that teacher')

            else:
                messages.info(request, 'That student cannot have a booking on that day')



    context = {'form':form}
    return render(request, 'crud/booking_form.html', context)













@login_required(login_url='login')
@allowed_users(allowed_roles=['teacher'])
def editBooking(request, pk):

    booking = Booking.objects.get(booking_id=pk)

    form = TeacherEditBookingForm(instance=booking)

    if request.method == 'POST':
        #print(request.POST)

        form = TeacherEditBookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            return redirect('bookings')


    context = {'form':form}
    return render(request, 'crud/booking_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'student'])
def deleteBooking(request, pk):

    booking = Booking.objects.get(booking_id=pk)

    if request.method == "POST":
        booking.delete()
        return redirect('bookings')


    context = {'item':booking}
    return render(request, 'crud/booking_delete.html', context)