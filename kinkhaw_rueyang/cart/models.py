from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Cart(models.Model):
    customer = models.OneToOneField(User, on_delete=models.PROTECT)
    shop = models.ForeignKey(
        "shop.Shop",
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )

class CartItem(models.Model):
    cart = models.ForeignKey(
        "cart.Cart",
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    menu = models.ForeignKey(
        "shop.Menu",
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
