from django.shortcuts import render
from django.views import View
from .models import *
from .forms import *
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

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
            "menu": query
        })
        