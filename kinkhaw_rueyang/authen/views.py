from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.contrib import messages
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import UserProfile 
from django.contrib.auth.forms import UserCreationForm


class RegisterView(View):
    def get(self, request):
        form = UserCreationForm() 
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
           
            user_profile = UserProfile.objects.create(user=user, role='customer')
            user_profile.save()

            login(request, user)  
            messages.success(request, "ลงทะเบียนสำเร็จ!")
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
