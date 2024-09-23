from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Order(models.Model):
    class Status(models.Choices):
        Order = "Order"
        Cooking = "Cooking"
        Completed = "Completed"
        Cancelled = "Cancelled"
    
    customer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    shop = models.ForeignKey(
        "shop.Shop",
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    total_price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    order_date = models.DateField(auto_now=False, auto_now_add=True)
    order_status = models.CharField(max_length=100, choices=Status.choices)

class OrderItem(models.Model):
    order = models.ForeignKey(
        "order.Order",
        on_delete=models.SET_NULL, 
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
