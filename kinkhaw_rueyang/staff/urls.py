from django.urls import path
from . import views

urlpatterns = [
    path("", views.AllShopView.as_view(), name="manageallshop"),
    path("search/", views.SearchShopView.as_view(), name="searchshop"),
    path("<int:shop_id>/", views.SelectShopView.as_view(), name="seeshopdetail"),
    path("user/", views.AllUserView.as_view(), name="managealluser"),
    path("user/customer/", views.CustomerGroupView.as_view(), name="customergroup"),
    path("user/shop/", views.ShopGroupView.as_view(), name="shopgroup"),
    path("user/search/", views.SearchUserView.as_view(), name="searchuser"),
]
