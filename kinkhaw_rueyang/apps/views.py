from django.shortcuts import redirect, render
from django.views import View
from .models import *
from .forms import *
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.db import transaction
from django.db.models import F, Q, Count, Sum
from django.contrib import messages
from django.utils import timezone

# class LoginView(View):
#     def get(self, request):
#         form = CustomerForm()
#         return render(request, 'login.html', {
#             'form': form,
#         })
    
#     def post(self, request):
#         form = CustomerForm(request.POST)
#         if form.is_valid():
#             return render(request, "test.html")
#         return render(request, "login.html", {
#             "form" : form
#         })

class SelectShopView(View):
    def get(self, request, customer_id):
        query2 = Customer.objects.get(id=customer_id)
        queries = Shop.objects.all()
        for query in queries:
            query.count_order = query.order_set.exclude(order_status__in=["Completed", "Cancelled"]).count()
        return render(request, "cus_select_shop.html", {
            "shop": queries,
            "cus": query2
        })

class SelectMenuView(View):
    def get(self, request, shop_id, customer_id):
        try:
            query = Menu.objects.filter(shop__id=shop_id)
            query2 = Shop.objects.get(id=shop_id)
            query3 = Customer.objects.get(id=customer_id)
        except ObjectDoesNotExist:
            return HttpResponse("<h1 style='font-size:100px'>ไม่พบร้านอาหารนี้ 🤔</h1>")
        return render(request, "cus_select_menu.html", {
            "menu": query,
            "shop": query2,
            "cus": query3
        })

class SelectMenuOrderView(View):
    def get(self, request, menu_id, shop_id, customer_id):
        try:
            query = Menu.objects.get(id=menu_id, shop__id=shop_id)
            query2 = Customer.objects.get(id=customer_id)
        except ObjectDoesNotExist:
            return HttpResponse("<h1 style='font-size:100px'>ไม่พบเมนูนี้ในร้านนี้😒🥲</h1>")
        return render(request, "cus_order_menu.html", {
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

class CartView(View):
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
        order = Order.objects.create(customer=cus, shop=cart.shop, total_price=cart.sum, order_date=timezone.now(), order_status="Order")
        # order_item = OrderItem.objects.create
        return redirect('selectshop', customer_id)
        

#ของน้องออม
class ManageMenuView(View):
    def get(self, request):
        menu_items = Menu.objects.all()
        categories = MenuCategory.objects.all()
        
        menu_with_categories = []
        for item in menu_items:
            category_names = [category.name for category in item.menucategory_set.all()]
            menu_with_categories.append({
                'item': item,
                'categories': category_names
            })
        
        return render(request, 'manage_menu.html', {'menu_with_categories': menu_with_categories, 'categories': categories})

class MenuCreateView(View):
    def get(self, request):
        form = MenuForm()
        categories = MenuCategory.objects.all()  
        return render(request, 'menu_form.html', {'form': form, 'categories': categories})

    def post(self, request):
        form = MenuForm(request.POST, request.FILES)
        if form.is_valid():
            menu_item = form.save()  
            category_ids = form.cleaned_data.get('categories')           
            if category_ids:
                menu_item.menu_category.set(category_ids)  
            return redirect('manage_menu')
        categories = MenuCategory.objects.all()
        return render(request, 'menu_form.html', {'form': form, 'categories': categories})



class MenuEditView(View):
    def get(self, request, pk):
        menu_item = Menu.objects.get(pk=pk)
        form = MenuForm(instance=menu_item)
        categories = MenuCategory.objects.all()
        selected_categories = menu_item.menucategory_set.all()  
        return render(request, 'menu_form.html', {
            'form': form,
            'categories': categories,
            'selected_categories': selected_categories
        })

    def post(self, request, pk):
        menu_item = Menu.objects.get(pk=pk)
        form = MenuForm(request.POST, request.FILES, instance=menu_item)
        if form.is_valid():
            menu_item = form.save()
            category_ids = form.cleaned_data.get('categories') 

            if category_ids:
               
                menu_item.menucategory_set.clear()  
                menu_item.menucategory_set.add(*category_ids)  
        categories = MenuCategory.objects.all()  
        return render(request, 'menu_form.html', {'form': form, 'categories': categories})

class MenuDeleteView(View):
    def post(self, request, pk):
        menu_item = Menu.objects.filter(pk=pk).first()
        if menu_item is None:
            return HttpResponse("<h1>ไม่พบเมนูนี้</h1>")
        
        try:
            with transaction.atomic():
                menu_item.delete()
            return redirect('manage_menu')
        except Exception as e:
            menu_items = Menu.objects.all()
            return render(request, 'manage_menu.html', {'menu_items': menu_items, 'error': str(e)})

# class MenuCategoryView(View):
#     def get(self, request, category_id):
#         category = MenuCategory.objects.filter(id=category_id).first()
#         if category is None:
#             return HttpResponse("<h1>ไม่พบหมวดหมู่ของเมนูนี้</h1>")
        
#         menus = category.menu.all()
#         return render(request, "menu_category.html", {'menus': menus, 'category': category})