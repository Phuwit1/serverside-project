# forms.py
from django import forms
from shop.models import *
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate


class MenuForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=MenuCategory.objects.all(),
        widget=forms.CheckboxSelectMultiple, 
        required=False,
        label="Categories"
    )
    
    shop = forms.ModelChoiceField(
        queryset=Shop.objects.all(),
        required=True,
        label="เลือกร้านค้า"
    )

    class Meta:
        model = Menu
        fields = ['name', 'price', 'description', 'image', 'categories']
