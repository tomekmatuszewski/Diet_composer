import pytest
from django.contrib.auth.models import User
from django.urls import resolve, reverse

from apps.recipes.models import Category, Recipe
from apps.recipes.views import (LikeView, RecipeCreateView, RecipeDeleteView,
                                RecipeDetailView, RecipesListView,
                                RecipeUpdateView)


@pytest.mark.django_db()
class TestUrls:
    @pytest.fixture(scope="class", name="user")
    def create_user_obj(self, django_db_blocker):
        with django_db_blocker.unblock():
            user = User.objects.create_user(username="testuser", password="test12345")
            yield user
        with django_db_blocker.unblock():
            user.delete()

    @pytest.fixture(scope="class", name="recipe")
    def create_recipe_obj(self, django_db_blocker, user):
        with django_db_blocker.unblock():
            category = Category.objects.create(name="cat1")
            recipe = Recipe.objects.create(
                title="Test recipe",
                description="Test description",
                author=user,
                preparation_time="10 min",
                ingredients="test ingredients",
                category=category,
            )
            yield recipe
        with django_db_blocker.unblock():
            recipe.delete()
            category.delete()

    def test_recipes_url(self):
        url = reverse("diet_composer-recipes")
        assert resolve(url).func.view_class == RecipesListView

    def test_recipe_detail_url(self, recipe):
        url = reverse("recipe-detail", kwargs={"pk": recipe.id})
        assert resolve(url).func.view_class == RecipeDetailView

    def test_create_recipe_url(self):
        url = reverse("recipe-create")
        assert resolve(url).func.view_class == RecipeCreateView

    def test_update_recipe_url(self, recipe):
        url = reverse("recipe-update", kwargs={"pk": recipe.id})
        assert resolve(url).func.view_class == RecipeUpdateView

    def test_delete_recipe_url(self, recipe):
        url = reverse("recipe-delete", kwargs={"pk": recipe.id})
        assert resolve(url).func.view_class == RecipeDeleteView

    def test_like_url(self, user):
        url = reverse("recipe-like", kwargs={"pk": user.pk})
        assert resolve(url).func == LikeView
