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
from .forms import *
from authen.models import *
from order.models import *
from datetime import datetime
from django.core.paginator import Paginator


class CreateShopView(View):
    def get(self, request):
        form = ShopForm()
        return render(request, 'create_shop.html', {'form': form})

    def post(self, request):
        form = ShopForm(request.POST)
        if form.is_valid():
            shop = form.save(commit=False)
            shop.shopkeeper = request.user
            shop.save()
            return redirect('shop')  
        return render(request, 'create_shop.html', {'form': form})

class ManageMenuView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    permission_required = []

    def get(self, request):
        shop = Shop.objects.filter(shopkeeper=request.user).first() 
        menu_items = Menu.objects.filter(shop=shop) 
        categories = MenuCategory.objects.filter(shop=shop) 

        menu_with_categories = []
        for item in menu_items:
            category_names = [category.name for category in item.menucategory_set.all()]
            menu_with_categories.append({
                'item': item,
                'categories': category_names
            })

        return render(request, 'manage_menu.html', {
            'menu_with_categories': menu_with_categories,
            'categories': categories,
            'shop_name': shop.name 
        })


class MenuCreateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    permission_required = []

    def get(self, request):
        shop = Shop.objects.filter(shopkeeper=request.user).first() 
        form = MenuForm(shop=shop)
        categories = MenuCategory.objects.filter(shop=shop)  
        return render(request, 'menu_form.html', {'form': form, 'categories': categories})

    def post(self, request):
        shop = Shop.objects.filter(shopkeeper=request.user).first() 
        form = MenuForm(request.POST, request.FILES, shop=shop)  

        if form.is_valid():
            menu_item = form.save(commit=False)
            menu_item.shop = shop 
            menu_item.save()

            category_ids = form.cleaned_data.get('categories')
            new_category_name = form.cleaned_data.get('new_category')

            if new_category_name:
                new_category, created = MenuCategory.objects.get_or_create(
                    name=new_category_name,
                    shop=shop
                )
                if created:
                    category_ids = list(category_ids) if category_ids else []
                    category_ids.append(new_category)

            if category_ids:
                menu_item.menucategory_set.set(category_ids)

            return redirect('shop')

        categories = MenuCategory.objects.filter(shop=shop)  
        return render(request, 'menu_form.html', {'form': form, 'categories': categories})

class MenuEditView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    permission_required = []

    def get(self, request, pk):
        menu_item = Menu.objects.get(pk=pk)
        shop = menu_item.shop  
        form = MenuForm(instance=menu_item, shop=shop) 
        categories = MenuCategory.objects.filter(shop=shop)  
        selected_categories = menu_item.menucategory_set.all()
        return render(request, 'menu_form.html', {
            'form': form,
            'categories': categories,
            'selected_categories': selected_categories,
            'shop_name': shop.name  
        })

    def post(self, request, pk):
        menu_item = Menu.objects.get(pk=pk)
        shop = menu_item.shop 
        form = MenuForm(request.POST, request.FILES, instance=menu_item, shop=shop) 

        if form.is_valid():
            menu_item = form.save(commit=False)
            menu_item.shop = shop
            menu_item.save()

            category_ids = form.cleaned_data.get('categories')
            new_category_name = form.cleaned_data.get('new_category')

            if new_category_name:
                new_category, created = MenuCategory.objects.get_or_create(
                    name=new_category_name,
                    shop=shop
                )
                if created:
                    category_ids = list(category_ids) if category_ids else []
                    category_ids.append(new_category)

            if category_ids:
                menu_item.menucategory_set.set(category_ids)

            return redirect('shop')

        categories = MenuCategory.objects.filter(shop=shop) 
        return render(request, 'menu_form.html', {'form': form, 'categories': categories})


class MenuDeleteView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    permission_required = []
    def post(self, request, pk):
        menu_item = Menu.objects.filter(pk=pk).first()
        if menu_item is None:
            return HttpResponse("<h1>ไม่พบเมนูนี้</h1>")
        
        try:
            with transaction.atomic():
                menu_item.delete()
            return redirect('shop')
        except Exception as e:
            menu_items = Menu.objects.all()
            return render(request, 'manage_menu.html', {'menu_items': menu_items, 'error': str(e)})

class ShopOrderView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    permission_required = []

    def get(self, request):
        user = request.user
        shop = Shop.objects.get(shopkeeper=user)
        orders = Order.objects.filter(shop=shop).order_by('-order_date').select_related('customer')
        order_count = Order.objects.filter(shop=shop).values('order_status').annotate(count=Count('order_status'))
        

        for order in orders:
            try:
                user_profile = order.customer.userprofile
                order.customer_full_name = f"{user_profile.first_name} {user_profile.last_name}"
                order.customer_phone = user_profile.phone_number
            except UserProfile.DoesNotExist:
                order.customer_full_name = "Unknown"
                order.customer_phone = None

        return render(request, "manage_order.html", {
            "orders": orders,
            "order_count": order_count,
        })
    def post(self, request):
        order_id = request.POST.get('orderid')
        action = request.POST.get('action')

        if action == 'cancel':
            order = Order.objects.get(id=order_id)
            order.delete()
            return redirect('manage_order')
        elif action == 'status':
            new_status = request.POST.get('new_status')
            if new_status in dict(Order.Status.choices).keys():
                order = Order.objects.get(id=order_id)
                order.order_status = new_status
                order.save()
            return redirect('manage_order')

class DailySummaryView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "daily_summary.html")
    
    def post(self, request):
        selected_date_str = request.POST.get('selected_date')
        selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date()

        shop = Shop.objects.get(shopkeeper=request.user)

        menu_summary = OrderItem.objects.filter(order__shop=shop, order__order_date=selected_date).values('menu__name').annotate(
            total_orders=Count('menu'),
            total_amount=Sum('price')
        )

        return render(request, "daily_summary.html", {
            "menu_summary": menu_summary,
            "selected_date": selected_date,
        })