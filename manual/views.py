from django.shortcuts import render, redirect
from .forms import ManualBookingForm
from main.models import *
from django.contrib import messages
from users.decorators import unauthenticated_user, allowed_users
from django.contrib.auth.decorators import login_required
from .mergeSort import *
from .extras import *
from users.decorators import *
import time

# Create your views here.

@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
#@valid_date
def manualType(request):

    try:

        student = request.user.student
        status = 'Pending'
        date = EveningDate.objects.get(year_group=student.year_group)
        timeslots =  date.timeslots.all()
        
        sortedTimeslots = date.timeslots.all().order_by('start_time')
        teachers = student.teachers.all()

        
        form = ManualBookingForm()

        form.fields['teacher'].queryset = student.teachers.all()
        form.fields['timeslot'].queryset = sortedTimeslots



        if request.method == 'POST':


            form = ManualBookingForm(request.POST)

            if form.is_valid():


                teacher = form.cleaned_data.get('teacher')
                timeslot = form.cleaned_data.get('timeslot')

                if Booking.objects.filter(student=student, timeslot=timeslot, date=date).count() == 0:

                    if Booking.objects.filter(teacher=teacher, timeslot=timeslot, date=date).count() == 0:

                        if Booking.objects.filter(teacher=teacher, student=student, date=date).count() == 0:

                            # Create an instance of the Booking model without saving it yet
                            booking = form.save(commit=False)

                            # Manually set the pre-filled fields
                            booking.student = student
                            booking.status = status
                            booking.date = date

                            # Save the booking
                            booking.save()
            

                            return redirect('userStudentBookings')
                        
                        else:
                            messages.info(request, 'You already have a booking with that teacher')
                            form.fields['teacher'].queryset = student.teachers.all()
                            form.fields['timeslot'].queryset = sortedTimeslots
                            

                    
                    else:
                        messages.info(request, 'That teacher already has a booking at that time')
                        form.fields['teacher'].queryset = student.teachers.all()
                        form.fields['timeslot'].queryset = sortedTimeslots
                
                else:
                    messages.info(request, 'You already have a booking at that time')
                    form.fields['teacher'].queryset = student.teachers.all()
                    form.fields['timeslot'].queryset = sortedTimeslots
        

        

        finalTimeslots = sortTimeslots(timeslots)

        teachersAv = teachersAvailability(teachers, finalTimeslots, date, student)

        

        context = {'form':form, 'timeslots':finalTimeslots, 'teachers':teachers, 'teachersAv':teachersAv}
        return render(request, 'manual/manual.html', context)
    
    except:
        return render(request, 'manual/error.html')







@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
#@valid_date
def studentEditManualType(request, pk):

    booking = Booking.objects.get(booking_id=pk)
    oldteacher = booking.teacher
    oldtimeslot = booking.timeslot

    student = request.user.student
    status = 'Pending'
    date = EveningDate.objects.get(year_group=student.year_group)
    timeslots =  date.timeslots.all()
    sortedTimeslots = date.timeslots.all().order_by('start_time')
    teachers = student.teachers.all()

    
    form = ManualBookingForm(instance=booking)

    form.fields['teacher'].queryset = student.teachers.all()
    form.fields['timeslot'].queryset = sortedTimeslots


    if request.method == 'POST':
        form = ManualBookingForm(request.POST, instance=booking)

        if form.is_valid():

            teacher = form.cleaned_data.get('teacher')
            timeslot = form.cleaned_data.get('timeslot')



            if teacher == oldteacher:
                if Booking.objects.filter(student=student, timeslot=timeslot, date=date).count() == 0:

                    if Booking.objects.filter(teacher=teacher, timeslot=timeslot, date=date).count() == 0:

                        form.save()
                        return redirect('userStudentBookings')
                        
                    else:
                        messages.info(request, 'That teacher already has a booking at that time')
                        form.fields['teacher'].queryset = student.teachers.all()
                        form.fields['timeslot'].queryset = sortedTimeslots
                
                else:
                    messages.info(request, 'You already have a booking at that time')
                    form.fields['teacher'].queryset = student.teachers.all()
                    form.fields['timeslot'].queryset = sortedTimeslots



            elif timeslot == oldtimeslot:
                if Booking.objects.filter(teacher=teacher, timeslot=timeslot, date=date).count() == 0:

                    if Booking.objects.filter(teacher=teacher, student=student, date=date).count() == 0:

                        form.save()
                        return redirect('userStudentBookings')
                        
                    else:
                        messages.info(request, 'You already have a booking with that teacher')
                        form.fields['teacher'].queryset = student.teachers.all()
                        form.fields['timeslot'].queryset = sortedTimeslots

                else:
                    messages.info(request, 'That teacher already has a booking at that time')
                    form.fields['teacher'].queryset = student.teachers.all()
                    form.fields['timeslot'].queryset = sortedTimeslots
            
            else:


                if Booking.objects.filter(student=student, timeslot=timeslot, date=date).count() == 0:

                    if Booking.objects.filter(teacher=teacher, timeslot=timeslot, date=date).count() == 0:

                        if Booking.objects.filter(teacher=teacher, student=student, date=date).count() == 0:

                            form.save()
                            return redirect('userStudentBookings')
                        
                        else:
                            messages.info(request, 'You already have a booking with that teacher')
                            form.fields['teacher'].queryset = student.teachers.all()
                            form.fields['timeslot'].queryset = sortedTimeslots

                    
                    else:
                        messages.info(request, 'That teacher already has a booking at that time')
                        form.fields['teacher'].queryset = student.teachers.all()
                        form.fields['timeslot'].queryset = sortedTimeslots
                
                else:
                    messages.info(request, 'You already have a booking at that time')
                    form.fields['teacher'].queryset = student.teachers.all()
                    form.fields['timeslot'].queryset = sortedTimeslots
    

    finalTimeslots = sortTimeslots(timeslots)

    teachersAv = teachersAvailability(teachers, finalTimeslots, date, student)
    

    context = {'form':form, 'timeslots':finalTimeslots, 'teachers':teachers, 'teachersAv':teachersAv}
    return render(request, 'manual/manual.html', context)