from django.views.generic import (ListView, DetailView)

from apps.recipes.models import Recipe


class RecipesListView(ListView):
    model = Recipe
    template_name = "recipes/recipes.html"
    context_object_name = "recipes"
    ordering = ["-date_public"]
    extra_context = {"title": "Recipes"}
    paginate_by = 4


class RecipeDetailView(DetailView):
    model = Recipe
