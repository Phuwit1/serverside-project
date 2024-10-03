from django.urls import path
from . import views

urlpatterns = [
    path("", views.AllShopView.as_view(), name="manageallshop"),
    path("search/", views.SearchShopView.as_view(), name="searchshop"),
    path("<int:shop_id>/", views.SelectShopView.as_view(), name="seeshopdetail"),
]
