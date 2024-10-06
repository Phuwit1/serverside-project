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
from order.models import Order, OrderItem
# Create your views here.
class CartView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    permission_required = ['cart.view_cart', 'cart.delete_cart']
    def get(self, request):
        try:
            cus = request.user
            query = Cart.objects.annotate(sum = Sum("cartitem__price")).get(customer__id=cus.id)
            return render(request, "cart.html", {
                'cart': query,
            })
        except ObjectDoesNotExist:
            return render(request, "cart.html", {
                'emp': 0,
            })
    
    @transaction.atomic
    def post(self, request):
        cus = request.user
        cart = Cart.objects.annotate(sum = Sum("cartitem__price")).get(customer__id=cus.id)
        orde = Order.objects.create(customer=cus, shop=cart.shop, total_price=cart.sum, order_date=timezone.now(), order_status="Order")
        for i in cart.cartitem_set.all():
            OrderItem.objects.create(order=orde, menu=i.menu, quantity=i.quantity, price=i.price)
        cart.delete()
        return redirect('selectshop')

class DeleteCartView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    permission_required = ['cart.view_cart', 'cart.delete_cart']
    @transaction.atomic
    def post(self, request, item_id):
        cus = request.user
        cartitem = CartItem.objects.get(cart__customer__id=cus.id, id=item_id)
        cart = cartitem.cart
        cartitem.delete()
        count_cart = cart.cartitem_set.count()
        if count_cart == 0:
            cart.delete()
        return redirect('customercart')

class CartItemView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    permission_required = ['cart.view_cartitem', 'cart.delete_cartitem', 'cart.change_cartitem']
    def get(self, request, item_id):
        cus = request.user
        cartitem = CartItem.objects.get(cart__customer__id=cus.id, id=item_id)
        return render(request, "cart_item.html", {"item": cartitem})
    def post(self, request, item_id):
        amount = int(request.POST.get('amount', 1))
        cus = request.user
        cartitem = CartItem.objects.get(cart__customer__id=cus.id, id=item_id)
        cartitem.quantity = amount
        cartitem.price = amount * cartitem.menu.price
        cartitem.save()
        return redirect('customercart')
