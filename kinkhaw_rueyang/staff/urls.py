from django.urls import path
from . import views

urlpatterns = [
    path("", views.AllShopView.as_view(), name="manageallshop"),
    path("<int:shop_id>/", views.SelectShopView.as_view(), name="seeshopdetail")
]
