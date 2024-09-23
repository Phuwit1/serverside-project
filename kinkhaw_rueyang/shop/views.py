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
from .forms import *

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


class MenuCreateView(View):
    def get(self, request):
        form = MenuForm()
        categories = MenuCategory.objects.all()  
        return render(request, 'menu_form.html', {'form': form, 'categories': categories})

    def post(self, request):
        form = MenuForm(request.POST, request.FILES)
        if form.is_valid():
            menu_item = form.save()  
            category_ids = form.cleaned_data.get('categories')           
            if category_ids:
                menu_item.menucategory_set.set(category_ids)
            return redirect('manage_menu')
        categories = MenuCategory.objects.all()
        return render(request, 'menu_form.html', {'form': form, 'categories': categories})



class MenuEditView(View):
    def get(self, request, pk):
        menu_item = Menu.objects.get(pk=pk)
        form = MenuForm(instance=menu_item)
        categories = MenuCategory.objects.all()
        selected_categories = menu_item.menucategory_set.all()  
        return render(request, 'menu_form.html', {
            'form': form,
            'categories': categories,
            'selected_categories': selected_categories
        })

    def post(self, request, pk):
        menu_item = Menu.objects.get(pk=pk)
        form = MenuForm(request.POST, request.FILES, instance=menu_item)
        if form.is_valid():
            menu_item = form.save()
            category_ids = form.cleaned_data.get('categories') 

            if category_ids:
                menu_item.menucategory_set.clear()  
                menu_item.menucategory_set.add(*category_ids)
            return redirect('manage_menu')  
        categories = MenuCategory.objects.all()  
        return render(request, 'menu_form.html', {'form': form, 'categories': categories})

class MenuDeleteView(View):
    def post(self, request, pk):
        menu_item = Menu.objects.filter(pk=pk).first()
        if menu_item is None:
            return HttpResponse("<h1>ไม่พบเมนูนี้</h1>")
        
        try:
            with transaction.atomic():
                menu_item.delete()
            return redirect('manage_menu')
        except Exception as e:
            menu_items = Menu.objects.all()
            return render(request, 'manage_menu.html', {'menu_items': menu_items, 'error': str(e)})
