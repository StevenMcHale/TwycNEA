from django.http import HttpResponse
from django.shortcuts import redirect
from main.models import *
from datetime import date, timedelta
from django.http import HttpResponseForbidden
import logging

logger = logging.getLogger(__name__)

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    
    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            logger.info(f"User: {request.user}, Request Path: {request.path}")

            group = getattr(request.user, 'cached_group', None)
            if group is None and request.user.groups.exists():
                group = request.user.groups.all()[0].name
                setattr(request.user, 'cached_group', group)  # Cache the group

            #group = None
            #if request.user.groups.exists():
            #    group = request.user.groups.all()[0].name
            
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            elif group == "teacher":
                return redirect('userTeacherBookings')
            elif group == "student":
                return redirect('userStudentBookings')
            elif group == "admin":
                return redirect('dashboard')
            elif group == "parent":
                return redirect('userParent')
        return wrapper_func
    return decorator


def valid_date(view_func):
    def wrapper_func(request, *args, **kwargs):

        student_yeargroup = request.user.student.year_group
        evening_date = EveningDate.objects.get(year_group=student_yeargroup).date

        today = date.today()  # Get today's date
        one_week_before = evening_date - timedelta(days=7)  # Calculate one week before the evening_date

        # Check if today is within one week before the evening_date
        if one_week_before <= today <= evening_date:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('userStudent')  # Redirect or handle as appropriate

    return wrapper_func