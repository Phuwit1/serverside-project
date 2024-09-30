<<<<<<< HEAD
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    USER_TYPE_CHOICES = (
        ('Customer', 'Customer'),
        ('Shop', 'Shop'),
    )
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, required=True, label="User Type")

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'user_type')
=======
from django import forms  #คิดว่าจะไม่ใช้formของdjango
from .models import UserProfile
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'first_name',
            'last_name',
            'phone_number',
            'email',
            'sex',
        ]
>>>>>>> 50d2a1a0e90c6b19a5eda5a49a7a90c71712b01e
