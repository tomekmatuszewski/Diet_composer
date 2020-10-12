from django.urls import path

from .views import (ProductCreateView, UserMenuListView, MenuCreateView,
                    ProductItemCreateView, ProductItemUpdateView, ProductItemDeleteView,
                    load_products, MenuDetailView, MenuUpdateView, MenuDeleteView,
                    MealCreateView)

urlpatterns = [
    path("menus/user/<str:username>", UserMenuListView.as_view(), name="user-menus"),
    path("product/new/", ProductCreateView.as_view(), name="product-create"),
    path("create-menu/", MenuCreateView.as_view(), name="create-menu"),
    path("menu/<int:pk>", MenuDetailView.as_view(), name="menu-details"),
    path("menu/<str:username>/<int:pk>/update/", MenuUpdateView.as_view(), name="menu-update"),
    path("menu/<str:username>/<int:pk>/delete/", MenuDeleteView.as_view(), name="menu-delete"),
    path("menu/<int:menu_id>/meal/<int:meal_id>/add-ingredient", ProductItemCreateView.as_view(),
         name="ingredient-create"),
    path("menu/<slug:menu_id>/ingredient/<int:pk>/edit", ProductItemUpdateView.as_view(), name="ingredient-edit"),
    path("menu/<slug:menu_id>/ingredient/<int:pk>/delete", ProductItemDeleteView.as_view(), name="ingredient-delete"),
    path("ajax/load-products/", load_products, name='ajax-load-products'),
    path("menu/<int:pk>/create-meal/", MealCreateView.as_view(), name="meal-create")
]
