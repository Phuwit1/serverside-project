from django.urls import path

from . import views

urlpatterns = [
    # path("login/", views.LoginView.as_view(), name="login"),
    path("selectshop/", views.SelectShopView.as_view(), name="selectshop"),
    path("selectshop/<int:shop_id>/menu/", views.SelectMenuView.as_view(), name="selectmenu"),
    path("selectshop/<int:shop_id>/menu/<int:menu_id>/", views.SelectMenuOrderView.as_view(), name="selectmenuorder"),
]
