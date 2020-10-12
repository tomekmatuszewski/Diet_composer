from django.urls import path

from .views import (ProductCreateView, UserMenuListView, MenuCreateView,
                    ProductItemCreateView, ProductItemUpdateView, load_products, MenuDetailView,
                    MealCreateView)

urlpatterns = [
    path("menus/user/<str:username>", UserMenuListView.as_view(), name="user-menus"),
    path("product/new/", ProductCreateView.as_view(), name="product-create"),
    path("create-menu/", MenuCreateView.as_view(), name="create-menu"),
    path("menu/<int:pk>", MenuDetailView.as_view(), name="menu-details"),
    path("menu/<int:pk>/new-meal/", MealCreateView.as_view(), name="meal-create"),
    path("menu/<int:menu_id>/meal/<int:meal_id>/add-ingredient", ProductItemCreateView.as_view(),
         name="ingredient-create"),
    path("menu/<slug:menu_id>/ingredient/<int:pk>/edit", ProductItemUpdateView.as_view(), name="ingredient-edit"),
    path("ajax/load-products/", load_products, name='ajax-load-products')
]
