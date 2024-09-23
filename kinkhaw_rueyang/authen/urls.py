from django.urls import path
from authen.views import *
from . import views
urlpatterns = [
    path('', views.LoginView.as_view(), name='login'),
    path('base/', views.BaseView.as_view(), name='base')
]
