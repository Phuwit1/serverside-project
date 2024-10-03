from django.shortcuts import redirect, render
from django.views import View
from shop.models import Shop
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# Create your views here.
class AllShopView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    permission_required = []
    def get(self, request):
        query = Shop.objects.all()
        return render(request, "manage_all_shop.html", {
            "shop": query
        })

class SelectShopView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    permission_required = []
    def get(self, request, shop_id):
        query = Shop.objects.get(id=shop_id)
        return render(request, "see_shop_detail.html", {
            "shop": query
        })
