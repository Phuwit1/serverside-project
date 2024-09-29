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
