from django.shortcuts import redirect, render
from django.views import View
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.db import transaction
from django.db.models import F, Q, Count, Sum
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class ManageMenuView(View):
    def get(self, request):
        menu_items = Menu.objects.all()
        categories = MenuCategory.objects.all()
        
        menu_with_categories = []
        for item in menu_items:
            category_names = [category.name for category in item.menucategory_set.all()]
            menu_with_categories.append({
                'item': item,
                'categories': category_names
            })
        
        return render(request, 'manage_menu.html', {'menu_with_categories': menu_with_categories, 'categories': categories})
