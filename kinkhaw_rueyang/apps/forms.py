from django import forms
from .models import *
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate



class CustomerForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    # class Meta:
    #     model = Customer
    #     fields =[
    #         'username',
    #         'password'
    #     ]
    #     widget = {
    #         'password': forms.PasswordInput()
    #     }
    def clean(self):
        clean_data = super().clean()
        usern = clean_data.get('username')
        passw = clean_data.get('password')
        if usern and passw:
            pass
            # ตรวจสอบว่ามี username และ password ตรงกับในฐานข้อมูลหรือไม่
            user = authenticate(username=usern, password=passw)
            if user is None:
                print(user)
                raise ValidationError("เข้าไม่ได้หรอก อิอิ")
        return clean_data
    
            