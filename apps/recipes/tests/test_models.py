import pytest
from django.contrib.auth.models import User

from apps.recipes.models import Category, Recipe


@pytest.mark.django_db()
class TestRecipe:
    @pytest.fixture(name="recipe", scope="class")
    def create_recipe(self, django_db_blocker, django_db_setup):
        with django_db_blocker.unblock():
            user = User.objects.create_user(
                username="test_user", email="test@demo.pl", password="test12345"
            )
            category = Category.objects.create(name="cat1")
            recipe = Recipe.objects.create(
                id=1,
                title="Test recipe",
                description="Test description",
                author=user,
                preparation_time="10 min",
                ingredients="test ingredients",
                category=category,
                total_calories=100,
                total_proteins=50,
                total_fats=50,
                total_carbohydrates=50
            )
        yield recipe
        with django_db_blocker.unblock():
            recipe.delete()
            category.delete()
            user.delete()

    def test_blog_obj_name(self, recipe):
        assert str(recipe) == "Test recipe"

    def test_recipe(self, recipe):
        assert isinstance(recipe, Recipe)
        assert recipe.title == "Test recipe"
        assert recipe.description == "Test description"
        assert recipe.author.username == "test_user"
        assert recipe.total_likes == 0
        assert recipe.category.name == "cat1"

    def test_get_absolute_url(self, recipe):
        assert recipe.get_absolute_url() == "/recipe/1/"
