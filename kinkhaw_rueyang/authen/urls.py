from django.urls import path
from authen.views import *
from . import views
urlpatterns = [
    path('', views.LoginView.as_view())
]
