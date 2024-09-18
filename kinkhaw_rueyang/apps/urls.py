from django.urls import path

from . import views

urlpatterns = [
    # path("login/", views.LoginView.as_view(), name="login"),
    path("selectshop/", views.SelectShopView.as_view(), name="selectshop"),
    path("selectshop/<int:shop_id>/menu/", views.SelectMenuView.as_view(), name="selectmenu"),
    path("selectshop/<int:shop_id>/menu/<int:menu_id>/", views.SelectMenuOrderView.as_view(), name="selectmenuorder"),
    path('managemenu/', views.ManageMenuView.as_view(), name='manage_menu'),
    path('managemenu/create/', views.MenuCreateView.as_view(), name='menu_create'),
    path('managemenu/edit/<int:pk>/', views.MenuEditView.as_view(), name='menu_edit'),
    path('managemenu/delete/<int:pk>/', views.MenuDeleteView.as_view(), name='menu_delete'),
]
