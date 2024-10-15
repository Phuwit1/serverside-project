from django.shortcuts import redirect, render
from django.views import View
from .models import *
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


class CreateShopView(View):
    def get(self, request):
        shop_form = ShopForm()  
        return render(request, 'create_shop.html', {'form': shop_form})

    def post(self, request):
        shop_form = ShopForm(request.POST)
        if shop_form.is_valid():
            new_shop = shop_form.save(commit=False) #create oj ยังไม่ลง DB
            new_shop.shopkeeper = request.user #ให้คนที่login เป็นเจ้าของร้าน
            new_shop.save()
            return redirect('shop')
        return render(request, 'create_shop.html', {'form': shop_form}) 


class ManageMenuView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    permission_required = ['shop.view_menu', 'shop.delete_menu', 'shop.change_menu']

    def get(self, request):
        user_shop = Shop.objects.filter(shopkeeper=request.user).first()  #ถ้าลบ .first ออกตอนเช็คต้องใช้ .exists
        if not user_shop:
            return redirect('create_shop')

        menus = Menu.objects.filter(shop=user_shop)
        menu_categories = MenuCategory.objects.filter(shop=user_shop)

        menu_data = [
            {
                'item': menu,
                'categories': [cat.name for cat in menu.menucategory_set.all()] #ชื่อ cat ของเมนู
            }
            for menu in menus
        ]

        return render(request, 'manage_menu.html', {
            'menu_with_categories': menu_data,
            'categories': menu_categories,
            'shop_name': user_shop.name,
        })


class MenuCreateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    permission_required = ['shop.add_menu', 'shop.add_menucategory']

    def get(self, request):
        user_shop = Shop.objects.filter(shopkeeper=request.user).first()
        categories = MenuCategory.objects.filter(shop=user_shop)  
        form = MenuForm()  
        form.fields['categories'].queryset  = categories
        return render(request, 'menu_form.html', {'form': form, 'categories': categories})

    def post(self, request):
        user_shop = Shop.objects.filter(shopkeeper=request.user).first()
        form = MenuForm(request.POST, request.FILES)

        if form.is_valid():
            menu_item = form.save(commit=False)
            menu_item.shop = user_shop
            menu_item.save()

            category_ids = form.cleaned_data.get('categories')
            new_category_name = form.cleaned_data.get('new_category')

            if new_category_name:
                new_category, created = MenuCategory.objects.get_or_create(
                    name=new_category_name, shop=user_shop
                )
                if created:
                    category_ids = list(category_ids) if category_ids else []
                    category_ids.append(new_category)

            if category_ids:
                menu_item.menucategory_set.set(category_ids)

            return redirect('shop')

        categories = MenuCategory.objects.filter(shop=user_shop)
        return render(request, 'menu_form.html', {'form': form, 'categories': categories})

class MenuEditView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    permission_required = ['shop.change_menu', 'shop.add_menucategory', 'shop.change_menucategory']

    def get(self, request, pk):
        menu_to_edit = Menu.objects.get(pk=pk)
        user_shop = menu_to_edit.shop

        categories = MenuCategory.objects.filter(shop=user_shop)

        menu_form = MenuForm(instance=menu_to_edit)
        menu_form.fields['categories'].queryset = categories  

        return render(request, 'menu_form.html', {
            'form': menu_form,
            'categories': categories,
            'shop_name': user_shop.name,
        })

    def post(self, request, pk):
        menu_to_edit = Menu.objects.get(pk=pk)
        user_shop = menu_to_edit.shop
        menu_form = MenuForm(request.POST, request.FILES, instance=menu_to_edit)

        if menu_form.is_valid():
            updated_menu_item = menu_form.save(commit=False)
            updated_menu_item.shop = user_shop
            updated_menu_item.save()

            selected_category_ids = menu_form.cleaned_data.get('categories')
            new_category_name = menu_form.cleaned_data.get('new_category')

            if new_category_name:
                new_category, created = MenuCategory.objects.get_or_create(
                    name=new_category_name, shop=user_shop
                )
                if created:
                    selected_category_ids = list(selected_category_ids or []) + [new_category]

            if selected_category_ids:
                updated_menu_item.menucategory_set.set(selected_category_ids)

            return redirect('shop')

        categories = MenuCategory.objects.filter(shop=user_shop)
        return render(request, 'menu_form.html', {
            'form': menu_form,
            'categories': categories,
        })




class MenuDeleteView(LoginRequiredMixin, View):
    login_url = '/authen/'
    
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
    permission_required = ['order.view_order']

    def get(self, request):
        user = request.user
        shop = Shop.objects.get(shopkeeper=user)
        orders = Order.objects.filter(shop=shop).order_by('-order_date', '-id').select_related('customer')
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
            order.order_status = 'Cancelled'
            order.save()

            
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

        menu_summary = OrderItem.objects.filter(
            order__shop=shop, 
            order__order_date=selected_date
        ).exclude(order__order_status='Cancelled').values(
            'menu__name'
        ).annotate(
            total_orders=Count('menu'), 
            total_amount=Sum('price')
        )

        total_sales = sum(item['total_amount'] for item in menu_summary)

        return render(request, "daily_summary.html", {
            "menu_summary": menu_summary,
            "selected_date": selected_date,
            "total_sales": total_sales,
        })