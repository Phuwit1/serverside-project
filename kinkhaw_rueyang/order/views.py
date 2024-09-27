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
from shop.models import Shop, Menu, MenuCategory
from cart.models import Cart, CartItem

class SelectShopView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    permission_required = []
    def get(self, request):
        queries = Shop.objects.all()
        for query in queries:
            query.count_order = query.order_set.exclude(order_status__in=["Completed", "Cancelled"]).count()
        return render(request, "select_shop.html", {
            "shop": queries
        })

class SelectMenuView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    permission_required = []
    def get(self, request, shop_id, category_id):
        try:
            if category_id == 0:
                query = Menu.objects.filter(shop__id=shop_id)
                query2 = Shop.objects.get(id=shop_id)
                query3 = MenuCategory.objects.filter(shop__id=shop_id)
            else:
                query = Menu.objects.filter(shop__id=shop_id, menucategory__id=category_id)
                query2 = Shop.objects.get(id=shop_id)
                query3 = MenuCategory.objects.filter(shop__id=shop_id)
        except ObjectDoesNotExist:
            return HttpResponse("<h1 style='font-size:100px'>ไม่พบร้านอาหารนี้ 🤔</h1>")
        return render(request, "select_menu.html", {
            "menu": query,
            "shop": query2,
            "category": query3,
        })

class SelectMenuOrderView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    permission_required = []
    def get(self, request, menu_id, shop_id):
        try:
            query = Menu.objects.get(id=menu_id, shop__id=shop_id)
            cart = Cart.objects.filter(customer__id=request.user.id).first()
        except ObjectDoesNotExist:
            return HttpResponse("<h1 style='font-size:100px'>ไม่พบเมนูนี้ในร้านนี้😒🥲</h1>")
        return render(request, "order_menu.html", {
            "menu": query,
            "cart": cart.shop.id if cart != None else 0,
        })
    
    @transaction.atomic
    def post(self, request, menu_id, shop_id):
        amount = int(request.POST.get('amount', 1))
        cus = request.user.id
        cart = Cart.objects.filter(customer__id=cus).first() #.first เพราะถ้าไม่มีจะreturn none
        if cart is None:
            shops = Shop.objects.get(id=shop_id)
            carts = Cart.objects.create(customer=request.user, shop=shops)
            menus = Menu.objects.get(id=menu_id)
            CartItem.objects.create(cart=carts, menu=menus, quantity=amount, price=menus.price*amount)
        else:
            carts = Cart.objects.get(customer__id=cus)
            if carts.shop.id == shop_id:
                menus = Menu.objects.get(id=menu_id)
                CartItem.objects.create(cart=carts, menu=menus, quantity=amount, price=menus.price*amount)
            else:
                carts.delete()
                shops = Shop.objects.get(id=shop_id)
                carts = Cart.objects.create(customer=request.user, shop=shops)
                menus = Menu.objects.get(id=menu_id)
                CartItem.objects.create(cart=carts, menu=menus, quantity=amount, price=menus.price*amount)
        return redirect('selectmenu', shop_id, 0)


class SelectMenuSearchView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    permission_required = []
    def post(self, request, shop_id):
        try:
            search = request.POST.get('search')
            query = Menu.objects.filter(shop__id=shop_id, name__icontains=search)
            query2 = Shop.objects.get(id=shop_id)
            query3 = MenuCategory.objects.filter(shop__id=shop_id)
        except ObjectDoesNotExist:
            return HttpResponse("<h1 style='font-size:100px'>ไม่พบร้านอาหารนี้ 🤔</h1>")
        return render(request, "select_menu.html", {
            "menu": query,
            "shop": query2,
            "category": query3,
        })

class OrderView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    permission_required = []
    def get(self, request, status):
        user = request.user
        if status == 'pending': 
            query = Order.objects.filter(customer__id=user.id).filter(Q(order_status="Order") | Q(order_status="Cooking")).order_by("-id")
            for i in query:
                i.order_count = Order.objects.filter(shop=i.shop, id__lt=i.id).filter(Q(order_status="Order") | Q(order_status="Cooking")).count()
            status = True
        elif status == 'completed':
            query = Order.objects.filter(customer__id=user.id, order_status='Completed').order_by('-id')
            status = False
        elif status == 'cancelled':
            query = Order.objects.filter(customer__id=user.id, order_status='Cancelled').order_by('-id')
            status = False
        return render(request, "view_order.html", {
            "order": query,
            "status": status,
        })
