from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Shop(models.Model):
    shopkeeper = models.ForeignKey(
        User,
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=10)
    address = models.TextField(null=True, blank=True)

class Menu(models.Model):
    shop = models.ForeignKey(
        "shop.Shop",
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)


class MenuCategory(models.Model):
    menu = models.ManyToManyField("shop.Menu")
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
