from django.forms import ModelForm
from main.models import *
from django.forms import CheckboxSelectMultiple
from django import forms



class BuildingForm(ModelForm):
    class Meta:
        model = Building
        fields = '__all__'

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'

class SubjectForm(ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'

class TimeslotForm(ModelForm):
    class Meta:
        model = Timeslot
        fields = '__all__'

class EveningDateForm(ModelForm):
    class Meta:
        model = EveningDate
        fields = '__all__'
    
    timeslots = forms.ModelMultipleChoiceField(
        queryset=Timeslot.objects.all(),
        widget=CheckboxSelectMultiple
    )

class TeacherForm(ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'
    
    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=CheckboxSelectMultiple
    )

    def __init__(self, *args, **kwargs):
        super(TeacherForm, self).__init__(*args, **kwargs)

        self.fields['subjects'].queryset = Subject.objects.all().order_by('name')


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
    
    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=CheckboxSelectMultiple
    )

    teachers = forms.ModelMultipleChoiceField(
        queryset=Teacher.objects.all(),
        widget=CheckboxSelectMultiple
    )

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        
        # Sort subjects and teachers alphabetically by their name
        self.fields['subjects'].queryset = Subject.objects.all().order_by('name')
        self.fields['teachers'].queryset = Teacher.objects.all().order_by('name')

    

class TeacherEditBookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = ['status']

class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'
        exclude = ['booking_id']



class ParentForm(ModelForm):
    class Meta:
        model = Parent
        fields = '__all__'
    
    students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.all(),
        widget=CheckboxSelectMultiple
    )

    def __init__(self, *args, **kwargs):
        super(ParentForm, self).__init__(*args, **kwargs)
        
        # Sort subjects and teachers alphabetically by their name
        self.fields['students'].queryset = Student.objects.all().order_by('name')

