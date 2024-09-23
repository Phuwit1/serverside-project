from django.urls import path
from . import views
urlpatterns = [
    path("", views.CartView.as_view(), name="customercart"),
    path("<int:item_id>/", views.CartItemView.as_view(), name="cartitemview"),
    path("<int:item_id>/delete/", views.DeleteCartView.as_view(), name='delete_cart_item'),
]

