from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # path("login/", views.LoginView.as_view(), name="login"),
    path("<int:customer_id>/selectshop/", views.SelectShopView.as_view(), name="selectshop"),
    path("<int:customer_id>/selectshop/<int:shop_id>/menu/", views.SelectMenuView.as_view(), name="selectmenu"),
    path("<int:customer_id>/selectshop/<int:shop_id>/menu/<int:menu_id>/", views.SelectMenuOrderView.as_view(), name="selectmenuorder"),
    path("<int:customer_id>/selectshop/cart/", views.CartView.as_view(), name="customercart"),
    
    path('managemenu/', views.ManageMenuView.as_view(), name='manage_menu'),
    path('managemenu/create/', views.MenuCreateView.as_view(), name='menu_create'),
    path('managemenu/edit/<int:pk>/', views.MenuEditView.as_view(), name='menu_edit'),
    path('managemenu/delete/<int:pk>/', views.MenuDeleteView.as_view(), name='menu_delete'),
    # path('managemenu/category/<int:category_id>/', views.MenuCategoryView.as_view(), name='menu_category') ไม่จำเป้นละมั้ง
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
