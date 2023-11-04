from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Student
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        
