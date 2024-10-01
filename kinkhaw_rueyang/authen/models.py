from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    SEX_CHOICE = (
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    sex = models.CharField(max_length=1, choices=SEX_CHOICE)
    address = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='userimage/', null=True, blank=True)

    def __str__(self):
        return self.user.username
