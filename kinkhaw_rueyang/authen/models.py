from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    SEX_CHOICE = (
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    )
    image = models.ImageField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    phone_number = models.CharField(max_length=10)
    email = models.EmailField()
    sex = models.CharField(choices=SEX_CHOICE)
    address = models.TextField()
    def __str__(self):
        return self.user.username
