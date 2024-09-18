from django.urls import path

from . import views

urlpatterns = [
    # path("login/", views.LoginView.as_view(), name="login"),
    path("selectshop/", views.SelectShopView.as_view(), name="selectshop")
]
