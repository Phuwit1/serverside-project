from django import forms
from .models import *
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth.models import auth


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields =[
            'username',
            'password'
        ]
        widget = {
            'password': forms.PasswordInput()
        }
    def clean(self):
        clean_data = super().clean()
        usern = clean_data.get('username')
        passw = clean_data.get('password')
        if usern and passw:
            # ตรวจสอบว่ามี username และ password ตรงกับในฐานข้อมูลหรือไม่
            user = auth.authenticate(username=usern, password=passw)
            if user is None:
                print(user)
                raise ValidationError("เข้าไม่ได้หรอก อิอิ")
        return clean_data
    
            