
from django.urls import path
from . import views
urlpatterns = [
    path('', views.ManageMenuView.as_view(), name='manage_menu'),
    path('managemenu/create/', views.MenuCreateView.as_view(), name='menu_create'),
    path('managemenu/edit/<int:pk>/', views.MenuEditView.as_view(), name='menu_edit'),
    path('managemenu/delete/<int:pk>/', views.MenuDeleteView.as_view(), name='menu_delete'),
]



