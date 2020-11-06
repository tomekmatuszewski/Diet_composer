import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from apps.diet_composer.models import RecipeItem, Meal, DailyMenu
from apps.recipes.models import Recipe, Category
from apps.users.models import UserActivity


@pytest.mark.django_db
class TestRecipeItemView:
    @pytest.fixture(name="user", scope="class")
    def create_user(self, django_db_blocker, django_db_setup):
        with django_db_blocker.unblock():
            user = User.objects.create_user(
                username="test_user", email="test@demo.pl", password="test12345"
            )
            activity = UserActivity.objects.create(factor=1.2, description="activity")
            activity.save()
            user.profile.age = 25
            user.profile.height = 190
            user.profile.gender = "Male"
            user.profile.weight = 80
            user.profile.activity = activity
            user.profile.save()

        yield user
        with django_db_blocker.unblock():
            user.delete()
            activity.delete()

    @pytest.fixture(name="recipe", scope="class")
    def create_recipe(self, django_db_blocker, django_db_setup, user):
        with django_db_blocker.unblock():
            category = Category.objects.create(name="testing cat")
            category.save()
            recipe = Recipe.objects.create(
                category=category,
                title="Recipe test",
                description="xxx",
                total_calories=100,
                total_proteins=50,
                total_fats=30,
                total_carbohydrates=50,
                preparation_time="10",
                ingredients="xxx",
                tags="Tag",
                author=user
            )
            recipe.save()
        yield recipe
        with django_db_blocker.unblock():
            recipe.delete()
            category.delete()

    @pytest.fixture(name="menu", scope="class")
    def create_menu(self, django_db_blocker, django_db_setup, user):
        with django_db_blocker.unblock():
            menu = DailyMenu.objects.create(
                name="test_menu",
                number_of_meals=2,
                author=user
            )
            menu.save()
            yield menu
        with django_db_blocker.unblock():
            menu.delete()

    @pytest.fixture(name="meal", scope="class")
    def create_meal(self, django_db_blocker, django_db_setup, menu):
        with django_db_blocker.unblock():
            meal = Meal.objects.create(
                name="test_meal"
            )
            meal.save()
            menu.meals.add(meal)
            yield meal

    def test_create_recipe_item(self, client, recipe, user, menu, meal):
        client.login(username="test_user", password="test12345")
        response = client.post(reverse("recipeitem-create", kwargs={"menu_id": menu.id, "meal_id": meal.id}),
                               data={
                                   "recipe_category": recipe.category.id,
                                   "recipe": recipe.id,
                                   "piece": 1,
                               })
        assert response.status_code == 302
        assert RecipeItem.objects.count() == 1

        id_ = RecipeItem.objects.first().id

        response = client.post(reverse("recipeitem-edit", kwargs={"menu_id": menu.id, "pk": id_}),
                               data={
                                   "recipe_category": recipe.category.id,
                                   "recipe": recipe.id,
                                   "piece": 0.5,
                               })
        assert response.status_code == 302
        assert RecipeItem.objects.first().piece == 0.5


    def test_delete_recipe_item(self, client, recipe, user, menu, meal):
        client.login(username="test_user", password="test12345")
        response = client.post(reverse("recipeitem-create", kwargs={"menu_id": menu.id, "meal_id": meal.id}),
                              data={
                                  "recipe_category": recipe.category.id,
                                  "recipe": recipe.id,
                                  "piece": 1,
                              })
        assert RecipeItem.objects.count() == 1

        id_ = RecipeItem.objects.first().id
        response = client.post(reverse("recipeitem-delete", kwargs={"menu_id": menu.id, "pk": id_}))
        assert response.status_code == 302
        assert RecipeItem.objects.count() == 0
