import pytest
from apps.diet_composer.models import RecipeItem
from apps.recipes.models import Recipe, Category
from django.contrib.auth.models import User


@pytest.mark.django_db()
class TestRecipeItem:
    @pytest.fixture(name="recipe_item", scope="class")
    def create_recipe_item(self, django_db_blocker, django_db_setup):
        with django_db_blocker.unblock():
            user = User.objects.create_user(
                username="test_user", email="test1@demo.pl", password="test12345"
            )
            category = Category.objects.create(name="cat1")
            recipe = Recipe.objects.create(
                title="Test recipe",
                description="Test description",
                author=user,
                preparation_time="10 min",
                ingredients="test ingredients",
                category=category,
                total_calories=100,
                total_proteins=50,
                total_fats=50,
                total_carbohydrates=50,
                tags="tag",
            )
            recipe_item = RecipeItem.objects.create(
                recipe_category=category, recipe=recipe, piece=1.5
            )
        yield recipe_item
        with django_db_blocker.unblock():
            recipe_item.delete()
            recipe.delete()
            category.delete()
            user.delete()

    def test_recipe_item_name(self, recipe_item):
        assert str(recipe_item) == "Test recipe item"

    def test_recipe_calories(self, recipe_item):
        assert recipe_item.calories == 150

    def test_recipe_proteins(self, recipe_item):
        assert recipe_item.proteins == 75

    def test_recipe_fats(self, recipe_item):
        assert recipe_item.fats == 75

    def test_recipe_carbohydrates(self, recipe_item):
        assert recipe_item.carbohydrates == 75
