from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .filters import BookingFilter
from django.contrib.auth.decorators import login_required
from users.decorators import unauthenticated_user, allowed_users
from manual.extras import *
from auto.extras import *

# Create your views here.


def home(request):
    return render(request, 'main/home.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def dashboard(request):
    lvi_students = Student.objects.filter(year_group="LVI").order_by('name')

    uvi_students = Student.objects.filter(year_group="UVI").order_by('name')

    parents = Parent.objects.all().order_by('name')

    teachers = Teacher.objects.all().order_by('name')

    subjects = Subject.objects.all().order_by('name')

    timeslots = Timeslot.objects.all()
    timeslots = sortTimeslots(timeslots)
    
    dates = EveningDate.objects.all()

    buildings = Building.objects.all().order_by('name')

    oldrooms = Room.objects.all()
    rooms = bubbleSortAlphaRooms(oldrooms)

    context = {'parents':parents, 'lvi_students':lvi_students, 'uvi_students':uvi_students, 'teachers':teachers, 'subjects':subjects, 'timeslots':timeslots, 'dates':dates, 'buildings':buildings, 'rooms':rooms}

    return render(request, 'main/dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'teacher'])
def bookings(request):
    bookings = Booking.objects.all()
    bookings = bookings.order_by('timeslot')

    total_bookings = bookings.count()
    complete = bookings.filter(status="Complete").count()
    pending = bookings.filter(status="Pending").count()

    myFilter = BookingFilter(request.GET, queryset=bookings)
    bookings = myFilter.qs

    context = {'bookings':bookings, 'total_bookings':total_bookings, 'complete':complete, 'pending':pending, 'myFilter':myFilter}

    return render(request, 'main/bookings.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def student(request, pk):
    student = Student.objects.get(id=pk)
    bookings = student.booking_set.all()
    total_bookings = bookings.count()
    subjects = student.subjects.all()
    teachers = student.teachers.all()

    finalBookings = sortBookings(bookings)

    context = {'student':student, 'bookings':finalBookings, 'total_bookings':total_bookings, 'subjects':subjects, 'teachers':teachers}

    return render(request, 'main/student.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def teacher(request, pk):
    teacher = Teacher.objects.get(id=pk)
    bookings = teacher.booking_set.all()
    total_bookings = bookings.count()
    subjects = teacher.subjects.all()
    students = Student.objects.filter(teachers__name=teacher.name)

    finalBookings = sortBookings(bookings)

    context = {'teacher':teacher, 'bookings':finalBookings, 'total_bookings':total_bookings, 'subjects':subjects, 'students':students}
    return render(request, 'main/teacher.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def room(request, pk):

    room = Room.objects.get(id=pk)
    teachers = room.teacher_set.all()


    context = {'room':room, 'teachers':teachers}
    return render(request, 'main/room.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def building(request, pk):

    building = Building.objects.get(id=pk)
    rooms = building.room_set.all()
    teachers = building.teacher_set.all()


    context = {'building':building, 'rooms':rooms, 'teachers':teachers}
    return render(request, 'main/building.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def subject(request, pk):

    subject = Subject.objects.get(id=pk)
    students = Student.objects.filter(subjects__name=subject.name)
    teachers = Teacher.objects.filter(subjects__name=subject.name)


    context = {'subject':subject, 'students':students, 'teachers':teachers}
    return render(request, 'main/subject.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def date(request, pk):

    date = EveningDate.objects.get(id=pk)
    timeslots = date.timeslots.all()

    finalTimeslots = sortTimeslots(timeslots)


    context = {'date':date, 'timeslots':finalTimeslots}
    return render(request, 'main/date.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def timeslot(request, pk):

    timeslot = Timeslot.objects.get(id=pk)
    dates = EveningDate.objects.filter(timeslots__start_time=timeslot.start_time)


    context = {'timeslot':timeslot, 'dates':dates}
    return render(request, 'main/timeslot.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def spreadsheetLVI(request):

    date = EveningDate.objects.get(year_group='LVI')
    timeslots =  date.timeslots.all()
    teachers = Teacher.objects.all()
    teachers = teachers.order_by('name')

    finalTimeslots = sortTimeslots(timeslots)
    teachersAv = adminteachersAvailability(teachers, finalTimeslots, date)

    context = {'timeslots':finalTimeslots, 'teachers':teachers, 'teachersAv':teachersAv}
    return render(request, 'main/sheetLVI.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def spreadsheetUVI(request):

    date = EveningDate.objects.get(year_group='UVI')
    timeslots =  date.timeslots.all()
    teachers = Teacher.objects.all()
    teachers = teachers.order_by('name')

    finalTimeslots = sortTimeslots(timeslots)
    teachersAv = adminteachersAvailability(teachers, finalTimeslots, date)

    context = {'timeslots':finalTimeslots, 'teachers':teachers, 'teachersAv':teachersAv}
    return render(request, 'main/sheetLVI.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def parent(request, pk):
    parent = Parent.objects.get(id=pk)
    students = parent.students.all()


    context = {'parent':parent, 'students':students}

    return render(request, 'main/parent.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
def map(request):


    context = {}

    return render(request, 'main/map.html', context)