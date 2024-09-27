from django.urls import path
from . import views
urlpatterns = [
    path("", views.SelectShopView.as_view(), name="selectshop"),
    path("<int:shop_id>/menu/category/<int:category_id>/", views.SelectMenuView.as_view(), name="selectmenu"),
    path("<int:shop_id>/menu/<int:menu_id>/", views.SelectMenuOrderView.as_view(), name="selectmenuorder"),
    path("<int:shop_id>/menu/search/", views.SelectMenuSearchView.as_view(), name="selectmenusearch"),
    path("myorder/<str:status>/", views.OrderView.as_view(), name="vieworder")
]
