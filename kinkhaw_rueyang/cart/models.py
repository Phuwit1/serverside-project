from django.db import models

# Create your models here.
class Cart(models.Model):
    customer = models.OneToOneField("apps.Customer", on_delete=models.PROTECT)
    shop = models.ForeignKey(
        "apps.Shop",
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )

class CartItem(models.Model):
    cart = models.ForeignKey(
        "apps.Cart",
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    menu = models.ForeignKey(
        "apps.Menu",
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
