from django.forms import ModelForm
from main.models import *

class ManualBookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = ['teacher', 'timeslot']

