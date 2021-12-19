from django import forms
from django.forms import TextInput
from django.forms.fields import EmailField
from django.forms.widgets import EmailInput, SelectDateWidget
from django.utils.regex_helper import Choice
from datetime import datetime


class RegisterForm(forms.Form):
    first_name = forms.CharField(label='First Name', widget=TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Last Name', widget=TextInput(attrs={'class': 'form-control'}))


class ProfileUpdateForm(forms.Form):
    username = forms.CharField(label="Username", widget=TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label="First Name", widget=TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label="Last Name", widget=TextInput(attrs={'class': 'form-control'}))


class AssignForm(forms.Form):
    assignment = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}))
    deadline = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))


class searchForm(forms.Form):
    class_name = forms.CharField(
        label='',
        widget=TextInput(
            attrs={'class': 'form-control rounded',
                   'placeholder': "Input the Class Mneumonic and/or Class Number ex) CS, CS3240, CS 3240"})
    )
    #
