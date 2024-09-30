from django.forms import ModelForm
from main.models import *

class TimeslotForm(ModelForm):
    class Meta:
        model = Timeslot
        fields = '__all__'