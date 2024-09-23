from django.urls import path
from . import views
urlpatterns = [
    path("", views.CartView.as_view(), name="customercart"),
    path("delete/<int:item_id>", views.DeleteCartView.as_view(), name='delete_cart_item'),
]

