from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

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


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    fields = ["title", "description", "image"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)