from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Teacher)
admin.site.register(Booking)
admin.site.register(Timeslot)
admin.site.register(EveningDate)
admin.site.register(Building)
admin.site.register(Room)
admin.site.register(Parent)