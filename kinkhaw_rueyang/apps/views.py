from django.shortcuts import render
from django.views import View
from .models import *
from .forms import *

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
