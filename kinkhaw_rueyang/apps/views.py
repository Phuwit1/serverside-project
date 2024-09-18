from django.shortcuts import redirect, render,get_object_or_404
from django.views import View
from .models import *
from .forms import *
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.db import transaction


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
    def get(self, request):
        queries = Shop.objects.all()
        for query in queries:
            query.count_order = query.order_set.exclude(order_status__in=["Completed", "Cancelled"]).count()
        return render(request, "select_shop.html", {
            "shop": queries,
        })

class SelectMenuView(View):
    def get(self, request, shop_id):
        try:
            query = Menu.objects.filter(shop__id=shop_id)
            query2 = Shop.objects.get(id=shop_id)
        except ObjectDoesNotExist:
            return HttpResponse("<h1 style='font-size:100px'>ไม่พบร้านอาหารนี้ 🤔</h1>")
        return render(request, "select_menu.html", {
            "menu": query,
            "shop": query2
        })

class SelectMenuOrderView(View):
    def get(self, request, menu_id, shop_id):
        try:
            query = Menu.objects.get(id=menu_id, shop__id=shop_id)
        except ObjectDoesNotExist:
            return HttpResponse("<h1 style='font-size:100px'>ไม่พบเมนูนี้ในร้านนี้😒🥲</h1>")
        return render(request, "order_menu.html", {
            "menu": query,
        })
    
    def post(self, request, menu_id, shop_id):
        amount = int(request.POST.get('amount', 1))
        print(amount)
        return redirect('selectmenu', shop_id)
    
#ของน้องออม
class ManageMenuView(View):
    def get(self, request):
        menu_items = Menu.objects.all()
        for item in menu_items:
            if not item.image:  
                item.image = 'default_image.jpg'  # รูปเหี้ยไรวะ
        return render(request, 'manage_menu.html', {'menu_items': menu_items})
    


class MenuCreateView(View):
    def get(self, request):
        form = MenuForm()
        return render(request, 'menu_form.html', {'form': form})

    def post(self, request):
        form = MenuForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                with transaction.atomic(): 
                    form.save()
                return redirect('manage_menu')
            except Exception as e:
                return render(request, 'menu_form.html', {'form': form, 'error': str(e)})
        return render(request, 'menu_form.html', {'form': form})

class MenuEditView(View):
    def get(self, request, pk):
        menu_item = get_object_or_404(Menu, pk=pk)
        form = MenuForm(instance=menu_item)
        return render(request, 'menu_form.html', {'form': form})

    def post(self, request, pk):
        menu_item = get_object_or_404(Menu, pk=pk)
        form = MenuForm(request.POST, request.FILES, instance=menu_item)
        if form.is_valid():
            try:
                with transaction.atomic():  
                    form.save()
                return redirect('manage_menu')
            except Exception as e:
                return render(request, 'menu_form.html', {'form': form, 'error': str(e)})
        return render(request, 'menu_form.html', {'form': form})

class MenuDeleteView(View):
    def get(self, request, pk):
        menu_item = get_object_or_404(Menu, pk=pk)
        return render(request, 'menu_confirm_delete.html', {'menu_item': menu_item})

    def post(self, request, pk):
        try:
            menu_item = get_object_or_404(Menu, pk=pk)
            with transaction.atomic():  
                menu_item.delete()
            return redirect('manage_menu')
        except Exception as e:
            return render(request, 'menu_confirm_delete.html', {'menu_item': menu_item, 'error': str(e)})
