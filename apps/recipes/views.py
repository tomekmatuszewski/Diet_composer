from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
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

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        stuff = get_object_or_404(Recipe, id=self.kwargs.get("pk"))
        total_likes = stuff.total_likes
        context["total_likes"] = total_likes
        return context


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    fields = ["category", "title", "preparing_time", "description", "ingredients", "image"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Recipe
    fields = ["category", "title", "preparing_time", "description", "ingredients", "image"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        recipe = self.get_object()
        if self.request.user == recipe.author:
            return True
        return False


class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipe
    success_url = "/recipes"

    def test_func(self):
        recipe = self.get_object()
        if self.request.user == recipe.author:
            return True
        return False


def LikeView(request, pk):

    recipe = get_object_or_404(Recipe, id=request.POST.get('recipe_id'))
    recipe.likes.add(request.user)
    return HttpResponseRedirect(reverse("recipe-detail", args=[str(pk)]))