
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.contrib import messages
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import UserProfileForm
from django.contrib.auth.models import Group
from .forms import UserProfileForm,RegisterForm
from .models import UserProfile
from shop.views import Shop
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

class RegisterView(View):
    def get(self, request):
        form = RegisterForm()  
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)  
        if form.is_valid():
            user = form.save()

            user_type = form.cleaned_data.get('user_type')
            UserProfile.objects.create(user=user)
            if user_type == 'Customer':
                group = Group.objects.get(name="Customer")
            else:
                group = Group.objects.get(name="Shop")

            group.user_set.add(user)

            login(request, user)
            return redirect('login')
        return render(request, 'register.html', {'form': form})
    
class LoginView(View):
    
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {"form": form})
    
    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('base')
        else:
            return render(request, 'login.html', {'form':form})


class LogoutView(View):
    
    def get(self, request):
        logout(request)
        return redirect('login')

class BaseView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    permission_required = []
    def get(self, request):
        return render(request, 'base.html')

class MyProfileView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    permission_required = []
    def get(self, request):
        try:
            use = request.user
            user = UserProfile.objects.get(user=use)
            form = UserProfileForm(instance=user)
        except ObjectDoesNotExist:
            return HttpResponse("<h1 style='font-size:100px'>ไม่พบUser Profileนี้ 🤨</h1>")
        return render(request, "myprofile.html", {
            'form': form,
            'user': user,
        })
    def post(self, request):
        user = UserProfile.objects.get(user__id=request.user.id)
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            user.save()
            return redirect('myprofile')
        return render(request, 'myprofile.html', {
            "form": form,
        })

class ShopRedirectView(LoginRequiredMixin, View):
    login_url = '/authen/'

    def get(self, request):
        user = request.user
        if user.groups.filter(name='Shop').exists():
            
            if Shop.objects.filter(shopkeeper=user).exists():
                return redirect('shop') 
            else:
                return redirect('create_shop')  
        else:
            return redirect('base')  
