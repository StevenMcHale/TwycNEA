from .mergeSort import *
from main.models import *

def sortTimeslots(pTimeslots):

    # Convert timeslots to strings
    oldStringTimeslots = []
    for timeslot in pTimeslots:
        oldStringTimeslots.append(str(timeslot))
    
    # Convert string timeslots to numbers
    numbersTimeslots = []

    for timeslot in oldStringTimeslots:
        timeslot = timeslot.replace(":", "")
        timeslot = int(timeslot)
        numbersTimeslots.append(timeslot)
    
    # Merge Sort
    mergeSort(numbersTimeslots)


    # Converted ordered numbers to string timeslots
    sortedTimeslots = []
    for item in numbersTimeslots:
        text = ""
        text += str(item)[0] + str(item)[1]
        text += ":"
        text += str(item)[2] + str(item)[3]
        text += ":"
        text += str(item)[4] + str(item)[5]
        sortedTimeslots.append(text)


    # create list of object timeslots in order
    finalTimeslots = []
    
    for item in sortedTimeslots:
        for timeslot in pTimeslots:
            if str(timeslot) == item:
                finalTimeslots.append(timeslot)
    
    return finalTimeslots


def sortBookings(pBookings):


    # Convert timeslots to strings
    oldStringTimeslots = []
    for booking in pBookings:
        oldStringTimeslots.append(str(booking.timeslot))
    
    # Convert string timeslots to numbers
    numbersTimeslots = []

    for timeslot in oldStringTimeslots:
        timeslot = timeslot.replace(":", "")
        timeslot = int(timeslot)
        numbersTimeslots.append(timeslot)
    
    # Merge Sort
    mergeSort(numbersTimeslots)


    # Converted ordered numbers to string timeslots
    sortedTimeslots = []
    for item in numbersTimeslots:
        text = ""
        text += str(item)[0] + str(item)[1]
        text += ":"
        text += str(item)[2] + str(item)[3]
        text += ":"
        text += str(item)[4] + str(item)[5]
        sortedTimeslots.append(text)


    # create list of object timeslots in order
    finalTimeslots = []

    
    for item in sortedTimeslots:
        for booking in pBookings:
            if str(booking.timeslot) == item and booking not in finalTimeslots:
                finalTimeslots.append(booking)
    
    return finalTimeslots




def teachersAvailability(pTeachers, pTimeslots, pDate, pStudent):

    teachersAv = []

    for teacher in pTeachers:
        teacherList = []
        teacherList.append(teacher.name)
        teacherList.append(teacher.room)
        teacherList.append(teacher.building)
        teacherList.append("|")
        for timeslot in pTimeslots:
            if teacher.booking_set.filter(teacher=teacher, timeslot=timeslot, date=pDate).count() == 0:
                teacherList.append(0)
            else:
                booking = Booking.objects.get(teacher=teacher, timeslot=timeslot, date=pDate)
                if booking.student.name == pStudent.name:
                    teacherList.append(pStudent.name)
                else:
                    teacherList.append(1)
        teachersAv.append(teacherList)
    
    return teachersAv


def adminteachersAvailability(pTeachers, pTimeslots, pDate):

    teachersAv = []

    for teacher in pTeachers:
        teacherList = []
        teacherList.append(teacher.name)
        teacherList.append(teacher.room)
        teacherList.append(teacher.building)
        teacherList.append("|")
        for timeslot in pTimeslots:
            if teacher.booking_set.filter(teacher=teacher, timeslot=timeslot, date=pDate).count() == 0:
                teacherList.append(0)
            else:
                booking = Booking.objects.get(teacher=teacher, timeslot=timeslot, date=pDate)
                teacherList.append(booking.student.name)
        teachersAv.append(teacherList)
    
    return teachersAv


def teachersAvailabilityAuto(pTeachers, pTimeslots, pDate):

    teachersAv = []

    for teacher in pTeachers:
        teacherList = []
        teacherList.append(teacher.name)
        for timeslot in pTimeslots:
            if teacher.booking_set.filter(teacher=teacher, timeslot=timeslot, date=pDate).count() == 0:
                teacherList.append(0)
            else:
                teacherList.append(1)
        teachersAv.append(teacherList)
    
    return teachersAv

