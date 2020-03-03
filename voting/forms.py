from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django import forms
from .models import *

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'is_student')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'is_student')

class StudentAddForm(UserCreationForm):
    username = forms.CharField(
        max_length=30,
        label = "Username",
    )

    firstname = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label = "Firstname",
    )

    lastname = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label = "Lastname",
    )

    level = forms.CharField(
        widget=forms.Select(
            choices = LEVEL,
            attrs={
                'class': 'browser-default custom-select',
            }
        ),
    )

    session = forms.CharField(
        widget=forms.Select(
            choices = SESSION,
        ),
    )

    faculty = forms.CharField(
        widget=forms.Select(
            choices = FACULTY,
        ),
    )

    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'type': 'email',
                'class': 'form-control',
            }
        ),
        label = "Email Address",
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser


    
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.first_name=self.cleaned_data.get('firstname') 
        user.last_name=self.cleaned_data.get('lastname')
        user.email=self.cleaned_data.get('email')
        user.save()
        student = Student.objects.create(
            user=user, 
            level=self.cleaned_data.get('level'), 
            session=self.cleaned_data.get('session'),
            faculty=self.cleaned_data.get('faculty'),
            )
        student.save()
        return user
