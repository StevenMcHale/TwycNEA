from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class CreateUserStudentForm(UserCreationForm):
    LEVEL_CHOICES = [
        ('LVI', 'Lower Sixth (LVI)'),
        ('UVI', 'Upper Sixth (UVI)'),
    ]
    level = forms.ChoiceField(choices=LEVEL_CHOICES, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'level']

class CreateUserTeacherForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CreateUserParentForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']