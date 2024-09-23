from django.shortcuts import redirect, render
from django.views import View
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.db import transaction
from django.db.models import F, Q, Count, Sum
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# Create your views here.
class CartView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    permission_required = []
    def get(self, request, customer_id):
        try:
            query = Cart.objects.annotate(sum = Sum("cartitem__price")).get(customer__id=customer_id)
            return render(request, "cus_cart.html", {
                'cart': query,
            })
        except ObjectDoesNotExist:
            return render(request, "cus_cart.html", {
                'emp': 0,
            })
    
    @transaction.atomic
    def post(self, request, customer_id):
        cart = Cart.objects.annotate(sum = Sum("cartitem__price")).get(customer__id=customer_id)
        cus = Customer.objects.get(id=customer_id)
        orde = Order.objects.create(customer=cus, shop=cart.shop, total_price=cart.sum, order_date=timezone.now(), order_status="Order")
        for i in cart.cartitem_set.all():
            OrderItem.objects.create(order=orde, menu=i.menu, quantity=i.quantity, price=i.price)
        cart.delete()
        return redirect('selectshop', customer_id)

class DeleteCartView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    permission_required = []
    @transaction.atomic
    def post(self, request, customer_id, item_id):
        cartitem = CartItem.objects.get(cart__customer__id=customer_id, id=item_id)
        cartitem.delete()
        return redirect('customercart', customer_id)
