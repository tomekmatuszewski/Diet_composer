from django.urls import path

from .views import (RecipesListView, RecipeDetailView, RecipeCreateView)

urlpatterns = [
    path("recipes/", RecipesListView.as_view(), name="diet_composer-recipes"),
    path("recipe/<int:pk>/", RecipeDetailView.as_view(), name="recipe-detail"),
    path("recipe/new", RecipeCreateView.as_view(), name="recipe-create"),
    ]