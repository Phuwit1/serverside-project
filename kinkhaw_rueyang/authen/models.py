from django.db import models
# from django.contrib.auth.models import User

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
