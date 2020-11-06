import pytest
from django.contrib.auth.models import User

from apps.diet_composer.models import Meal, ProductCategory, Product
from apps.recipes.models import Recipe, Category


@pytest.mark.django_db()
class TestMeal:
    @pytest.fixture(name="meal", scope="class")
    def create_meal(self, django_db_blocker, django_db_setup):
        with django_db_blocker.unblock():
            user = User.objects.create_user(
                username="test_user", email="test@demo.pl", password="test12345"
            )
            product_category = ProductCategory.objects.create(name="Test Category")
            product = Product.objects.create(
                category=product_category,
                name="Test Product",
                calories_per_100=100,
                proteins_per_100=50,
                fats_per_100=50,
                carbohydrates_per_100=50,
                weight_of_pcs=100,
                author=user,
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
            meal = Meal.objects.create(name="Test Meal")
            meal.save()
            meal.ingredients.create(
                product=product, category=product_category, unit="g", weight=100
            )
            meal.recipes.create(recipe=recipe, recipe_category=category, piece=1)

        yield meal
        with django_db_blocker.unblock():
            product.delete()
            recipe.delete()
            product_category.delete()
            category.delete()
            meal.delete()
            user.delete()

    def test_meal_name(self, meal):
        assert str(meal) == "Test Meal"

    def test_meal_calories(self, meal):
        assert meal.total_calories == 200

    def test_meal_proteins(self, meal):
        assert meal.total_proteins == 100

    def test_meal_fats(self, meal):
        assert meal.total_fats == 100

    def test_meal_carbo(self, meal):
        assert meal.total_carbohydrates == 100
