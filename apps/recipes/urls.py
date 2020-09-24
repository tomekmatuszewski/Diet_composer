from django.urls import path

from .views import RecipesListView

urlpatterns = [
    path("recipes/", RecipesListView.as_view(), name="diet_composer-recipes"),
    ]