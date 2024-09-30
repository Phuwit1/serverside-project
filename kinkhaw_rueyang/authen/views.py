from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.contrib import messages
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import UserProfileForm
from django.contrib.auth.models import Group
from .forms import UserProfileForm

class RegisterView(View):
    def get(self, request):
        form = UserProfileForm()  
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = UserProfileForm(request.POST)  
        if form.is_valid():
            user = form.save()

            user_type = form.cleaned_data.get('user_type')
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
        return render(request, 'login.html', {"form": None})
    
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
        user = request.user
        form = UserProfileForm(instance=user)
        return render(request, "myprofile.html", {
            'form': form
        })
