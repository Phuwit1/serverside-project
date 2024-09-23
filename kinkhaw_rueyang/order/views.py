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
from shop.models import Shop, Menu
from cart.models import Cart, CartItem

class SelectShopView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    permission_required = []
    def get(self, request):
        user = request.user
        queries = Shop.objects.all()
        for query in queries:
            query.count_order = query.order_set.exclude(order_status__in=["Completed", "Cancelled"]).count()
        return render(request, "select_shop.html", {
            "shop": queries
        })

class SelectMenuView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    permission_required = []
    def get(self, request, shop_id):
        try:
            query = Menu.objects.filter(shop__id=shop_id)
            query2 = Shop.objects.get(id=shop_id)
            query3 = request.user
        except ObjectDoesNotExist:
            return HttpResponse("<h1 style='font-size:100px'>ไม่พบร้านอาหารนี้ 🤔</h1>")
        return render(request, "select_menu.html", {
            "menu": query,
            "shop": query2,
            "cus": query3
        })

class SelectMenuOrderView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    permission_required = []
    def get(self, request, menu_id, shop_id):
        try:
            query = Menu.objects.get(id=menu_id, shop__id=shop_id)
            query2 = request.user
        except ObjectDoesNotExist:
            return HttpResponse("<h1 style='font-size:100px'>ไม่พบเมนูนี้ในร้านนี้😒🥲</h1>")
        return render(request, "order_menu.html", {
            "menu": query,
            "cus": query2,
        })
    
    @transaction.atomic
    def post(self, request, menu_id, shop_id, customer_id):
        amount = int(request.POST.get('amount', 1))
        cart = Cart.objects.filter(customer__id=customer_id).first() #.first เพราะถ้าไม่มีจะreturn none
        if cart is None:
            cus = Customer.objects.get(id=customer_id)
            shops = Shop.objects.get(id=shop_id)
            carts = Cart.objects.create(customer=cus, shop=shops)
            menus = Menu.objects.get(id=menu_id)
            CartItem.objects.create(cart=carts, menu=menus, quantity=amount, price=menus.price*amount)
        else:
            carts = Cart.objects.get(customer__id=customer_id)
            if carts.shop.id == shop_id:
                menus = Menu.objects.get(id=menu_id)
                CartItem.objects.create(cart=carts, menu=menus, quantity=amount, price=menus.price*amount)
            else:
                carts.delete()
                messages.warning(request, 'อาหารในcartจะถูกลบเนื่องจากคุณทำการเปลี่ยนร้าน')
                cus = Customer.objects.get(id=customer_id)
                shops = Shop.objects.get(id=shop_id)
                carts = Cart.objects.create(customer=cus, shop=shops)
                menus = Menu.objects.get(id=menu_id)
                CartItem.objects.create(cart=carts, menu=menus, quantity=amount, price=menus.price*amount)
        return redirect('selectmenu', customer_id, shop_id)
