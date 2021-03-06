from django.urls import path

from .views import (
    MealCreateView,
    MealDeleteView,
    MenuCreateView,
    MenuDeleteView,
    MenuDetailView,
    MenuUpdateView,
    ProductCreateView,
    ProductDeleteView,
    ProductItemCreateView,
    ProductItemDeleteView,
    ProductItemUpdateView,
    ProductListView,
    ProductUpdateView,
    RecipeItemCreateView,
    RecipeItemDeleteView,
    RecipeItemUpdateView,
    UserMenuListView,
    load_products,
    load_recipes,
)

urlpatterns = [
    path("menus/user/<str:username>", UserMenuListView.as_view(), name="user-menus"),
    path("product/new/", ProductCreateView.as_view(), name="product-create"),
    path("products/<str:username>/", ProductListView.as_view(), name="products-list"),
    path(
        "product/<int:pk>/update/", ProductUpdateView.as_view(), name="product-update"
    ),
    path(
        "product/<int:pk>/delete/", ProductDeleteView.as_view(), name="product-delete"
    ),
    path("create-menu/", MenuCreateView.as_view(), name="create-menu"),
    path("menu/<int:pk>", MenuDetailView.as_view(), name="menu-details"),
    path(
        "menu/<str:username>/<int:pk>/update/",
        MenuUpdateView.as_view(),
        name="menu-update",
    ),
    path(
        "menu/<str:username>/<int:pk>/delete/",
        MenuDeleteView.as_view(),
        name="menu-delete",
    ),
    path(
        "menu/<int:menu_id>/meal/<int:meal_id>/add-ingredient",
        ProductItemCreateView.as_view(),
        name="ingredient-create",
    ),
    path(
        "menu/<slug:menu_id>/ingredient/<int:pk>/edit",
        ProductItemUpdateView.as_view(),
        name="ingredient-edit",
    ),
    path(
        "menu/<slug:menu_id>/ingredient/<int:pk>/delete",
        ProductItemDeleteView.as_view(),
        name="ingredient-delete",
    ),
    path("ajax/load-products/", load_products, name="ajax-load-products"),
    path("menu/<int:pk>/create-meal/", MealCreateView.as_view(), name="meal-create"),
    path("menu/<slug:menu_id>/meal/<int:pk>/delete", MealDeleteView.as_view(), name="meal-delete"),
    path(
        "menu/<int:menu_id>/meal/<int:meal_id>/add-recipe",
        RecipeItemCreateView.as_view(),
        name="recipeitem-create",
    ),
    path(
        "menu/<slug:menu_id>/recipe/<int:pk>/edit",
        RecipeItemUpdateView.as_view(),
        name="recipeitem-edit",
    ),
    path(
        "menu/<slug:menu_id>/recipe/<int:pk>/delete",
        RecipeItemDeleteView.as_view(),
        name="recipeitem-delete",
    ),
    path("ajax/load-recipes/", load_recipes, name="ajax-load-recipes"),
]
