# forms.py
from django import forms
from shop.models import *
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate


class MenuForm(forms.ModelForm):
    
    new_category = forms.CharField(
        max_length=100, 
        required=False, 
        label="Add New Category"
    )
    
    categories = forms.ModelMultipleChoiceField(
        queryset=MenuCategory.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Categories"
    )
    
    # shop = forms.ModelChoiceField(
    #     queryset=Shop.objects.all(),
    #     required=True,
    #     label="เลือกร้านค้า"
    # )  เปลี่ยนเป็นแสดงชื่อร้านที่เราloginเข้ามา

    

    class Meta:
        model = Menu
        fields = ['name', 'price', 'description', 'image', 'categories', 'new_category', 'shop']


class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['name', 'description', 'phone_number', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ชื่อร้าน'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'คำอธิบายร้าน'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'หมายเลขโทรศัพท์'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'ที่อยู่'}),
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number.isdigit() or len(phone_number) != 10:
            raise forms.ValidationError("หมายเลขโทรศัพท์ต้องเป็นตัวเลข 10 หลัก")
        return phone_number