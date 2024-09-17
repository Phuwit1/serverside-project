from django.shortcuts import render
from django.views import View
from .models import *
from .forms import *
# Create your views here.
class LoginView(View):
    def get(self, request):
        form = CustomerForm()
        return render(request, 'login.html', {
            'form': form,
        })
    