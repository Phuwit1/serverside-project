from django.shortcuts import redirect, render
from django.views import View
from shop.models import Shop
from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# Create your views here.
class AllShopView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    permission_required = ['shop.view_shop', 'shop.delete_shop']
    def get(self, request):
        query = Shop.objects.all()
        return render(request, "manage_all_shop.html", {
            "shop": query
        })
        
    def post(self, request):
        shop_id = request.POST.get('shopid')
        shop = Shop.objects.get(id=shop_id)
        shop.delete()
        return redirect('manageallshop')

class SelectShopView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    permission_required = ['shop.view_shop', 'shop.delete_shop']
    def get(self, request, shop_id):
        query = Shop.objects.get(id=shop_id)
        return render(request, "see_shop_detail.html", {
            "shop": query
        })

class SearchShopView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    permission_required = ['shop.view_shop', 'shop.delete_shop']
    def post(self, request):
        query = Shop.objects.filter(name__icontains=request.POST.get('search'))
        return render(request, "manage_all_shop.html", {
            "shop": query
        })

class AllUserView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    permission_required = ['auth.view_user', 'auth.change_user']
    def get(self, request):
        query = User.objects.filter(is_staff=False)
        for i in query:
            i.group = [j.name for j in i.groups.all()]
        return render(request, "manage_all_user.html", {
            "user": query
        })


class CustomerGroupView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    permission_required = ['auth.change_group']
    def post(self, request):
        user = User.objects.get(id=request.POST.get('use'))
        groups = [i for i in user.groups.all()]
        group = Group.objects.get(name="Customer")
        if group in groups:
            user.groups.remove(group)
        else:
            user.groups.add(group)
        return redirect("managealluser")

class ShopGroupView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    permission_required = ['auth.change_group']
    def post(self, request):
        user = User.objects.get(id=request.POST.get('use'))
        groups = [i for i in user.groups.all()]
        group = Group.objects.get(name="Shop")
        if group in groups:
            user.groups.remove(group)
        else:
            user.groups.add(group)
        return redirect("managealluser")

class SearchUserView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    permission_required = ['auth.view_user', 'auth.change_user']
    def post(self, request):
        search = request.POST.get('search')
        query = User.objects.filter(username__icontains=search, is_staff=False)
        for i in query:
            i.group = [j.name for j in i.groups.all()]
        return render(request, "manage_all_user.html", {
            "user": query
        })
