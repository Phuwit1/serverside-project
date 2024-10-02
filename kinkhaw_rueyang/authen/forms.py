from django import forms 
from .models import UserProfile
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile
from django.utils import timezone
from django.core.exceptions import ValidationError

class RegisterForm(UserCreationForm):
    USER_TYPE_CHOICES = (
        ('Customer', 'Customer'),
        ('Shop', 'Shop'),
    )
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, required=True, label="User Type")

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'user_type')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'first_name',
            'last_name',
            'birth_date',
            'phone_number',
            'email',
            'sex',
            'address',
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        bd = cleaned_data.get('birth_date')
        phone = cleaned_data.get('phone_number')
        if bd > timezone.now().date():
            raise ValidationError("ห้ามเป็นวันในอนาคต")
        if phone.isdigit() == False:
            raise ValidationError("เบอร์โทรศัพท์ต้องเป็นตัวเลขเท่านั้น")
        elif len(phone) != 10:
            raise ValidationError("เบอร์โทรศัพท์มือถือต้องมี10ตัวอักษร")
        
