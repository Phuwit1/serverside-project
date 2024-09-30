from django.db import models
# from django.contrib.auth.models import User

<<<<<<< HEAD
# class UserProfile(models.Model):
#     ROLES = (
#         ('customer', 'Customer'),
#         ('shopkeeper', 'Shopkeeper'),
#         ('staff', 'Staff'),
#     )
#     user = models.OneToOneField(User, on_delete=models.CASCADE)  # แก้ไข indent ที่นี่
#     role = models.CharField(max_length=20, choices=ROLES, default='customer')

#     def __str__(self):
#         return self.user.username
=======
class UserProfile(models.Model):
    SEX_CHOICE = (
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)
    email = models.EmailField()
    sex = models.CharField(choices=SEX_CHOICE)
    def __str__(self):
        return self.user.username
>>>>>>> 50d2a1a0e90c6b19a5eda5a49a7a90c71712b01e
