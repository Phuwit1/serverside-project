from django.urls import path
from .views import *
from . import views
urlpatterns = [
    # path('')
    path('', RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('base/', views.BaseView.as_view(), name='base'),
    path('myprofile/', views.MyProfileView.as_view(), name="myprofile"),
]
