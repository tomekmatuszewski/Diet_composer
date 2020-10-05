from django.urls import path

from .views import (LikeView, RecipeCreateView, RecipeDeleteView,
                    RecipeDetailView, RecipesListView, RecipeUpdateView)

urlpatterns = [
    path("recipes/", RecipesListView.as_view(), name="diet_composer-recipes"),
    path("recipe/<int:pk>/", RecipeDetailView.as_view(), name="recipe-detail"),
    path("recipe/new", RecipeCreateView.as_view(), name="recipe-create"),
    path("recipe/<int:pk>/update/", RecipeUpdateView.as_view(), name="recipe-update"),
    path("recipe/<int:pk>/delete/", RecipeDeleteView.as_view(), name="recipe-delete"),
    path("recipe-like/<int:pk>", LikeView, name="recipe-like"),
]
