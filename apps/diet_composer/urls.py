from django.urls import path

from .views import (ProductCreateView, UserMenuListView, MenuCreateView, ProductItemCreateView, load_products, MenuDetailView)

urlpatterns = [
    path("menus/user/<str:username>", UserMenuListView.as_view(), name="user-menus"),
    path("product/new/", ProductCreateView.as_view(), name="product-create"),
    path("create-menu/", MenuCreateView.as_view(), name="create-menu"),
    path("menu/<int:pk>", MenuDetailView.as_view(), name="menu-details"),
    path("ingredient/new/", ProductItemCreateView.as_view(), name="ingredient-create"),
    path("ajax/load-products/", load_products, name='ajax-load-products')
]
