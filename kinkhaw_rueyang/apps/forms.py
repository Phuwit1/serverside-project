# forms.py
from django import forms
from .models import *
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate



# class CustomerForm(forms.Form):
#     username = forms.CharField()
#     password = forms.CharField()
    # class Meta:
    #     model = Customer
    #     fields =[
    #         'username',
    #         'password'
    #     ]
    #     widget = {
    #         'password': forms.PasswordInput()
    #     }
    # def clean(self):
    #     clean_data = super().clean()
    #     usern = clean_data.get('username')
    #     passw = clean_data.get('password')
    #     if usern and passw:
    #         pass
    #         # ตรวจสอบว่ามี username และ password ตรงกับในฐานข้อมูลหรือไม่
    #         user = authenticate(username=usern, password=passw)
    #         if user is None:
    #             print(user)
    #             raise ValidationError("เข้าไม่ได้หรอก อิอิ")
    #     return clean_data
    
class MenuForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=MenuCategory.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # สามารถเปลี่ยนเป็น Dropdown หรือ SelectMultiple
        required=False,  # ทำให้เป็นตัวเลือก ไม่บังคับต้องเลือก
        label="Categories"  # ป้ายชื่อของฟิลด์นี้
    )

    class Meta:
        model = Menu
        fields = ['name', 'price', 'description', 'image', 'categories']
