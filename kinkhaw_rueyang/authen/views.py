
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.contrib import messages
from django.views import View
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import UserProfileForm
from django.contrib.auth.models import Group
from .forms import UserProfileForm,RegisterForm
from .models import UserProfile
from shop.views import Shop
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.contrib.auth import update_session_auth_hash

class RegisterView(View):
    def get(self, request):
        form = RegisterForm()  
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)  
        if form.is_valid():
            user = form.save()
            select_type = form.cleaned_data.get('user_type') #เอาจากform
            UserProfile.objects.create(user=user)
            if select_type == 'Customer':
                group = Group.objects.get(name="Customer")
            else:
                group = Group.objects.get(name="Shop")

            group.user_set.add(user)

            login(request, user)
            return redirect('myprofile')
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
    


class BaseView(LoginRequiredMixin, View):
    login_url = '/authen/'

    def get(self, request):
        is_customer = request.user.groups.filter(name='Customer').exists()
        is_shop = request.user.groups.filter(name='Shop').exists()
        is_staff = request.user.groups.filter(name='Staff').exists()  

        context = {
            'user': request.user,
            'is_customer': is_customer,
            'is_shop': is_shop,
            'is_staff': is_staff,
        }
        return render(request, 'base.html', context)

class MyProfileView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    permission_required = ['authen.view_userprofile', 'authen.change_userprofile']
    def get(self, request):
        try:
            use = request.user
            users = UserProfile.objects.get(user=use)
            form = UserProfileForm(instance=users)
        except ObjectDoesNotExist:
            UserProfile.objects.create(user=request.user)
            return redirect("myprofile")
        return render(request, "myprofile.html", {
            'form': form,
            'users': users,
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

class ChangePasswordView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    permission_required = ['authen.change_userprofile']
    
    def get(self, request):
        form = PasswordChangeForm(request.user)
        # form = UserChangePassword(request.user)
        return render(request, 'changepass.html', {
            'form': form
        })
    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('myprofile')
        return render(request, 'changepass.html', {
            'form': form
        })
