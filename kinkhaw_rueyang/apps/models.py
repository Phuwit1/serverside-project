from django.db import models

# Create your models here.
class Customer(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

class Customer_Detail(models.Model):
    customer = models.OneToOneField("apps.Customer", on_delete=models.PROTECT)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=10)
    email = models.EmailField()

class Shopkeeper(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

class Shop(models.Model):
    shopkeeper = models.ForeignKey(
        "apps.Shopkeeper",
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=10)
    address = models.TextField(null=True, blank=True)

class Order(models.Model):
    class Status(models.Choices):
        Order = "Order"
        Cooking = "Cooking"
        Completed = "Completed"
        Cancelled = "Cancelledd"
    
    customer = models.ForeignKey(
        "apps.Customer",
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    shop = models.ForeignKey(
        "apps.Shop",
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    total_price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    order_date = models.DateField(auto_now=False, auto_now_add=True)
    order_status = models.CharField(max_length=100, choices=Status.choices)

class Menu(models.Model):
    shop = models.ForeignKey(
        "apps.Shop",
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True) #not sure


class OrderItem(models.Model):
    order = models.ForeignKey(
        "apps.Order",
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    menu = models.ForeignKey( #not sure
        "apps.Menu",
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2)

class MenuCategory(models.Model):
    menu = models.ManyToManyField("apps.Menu")
    name = models.CharField(max_length=100)
