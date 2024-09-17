from django import forms
from .models import *
from django.forms import ModelForm

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields =[
            'username',
            'password'
        ]
