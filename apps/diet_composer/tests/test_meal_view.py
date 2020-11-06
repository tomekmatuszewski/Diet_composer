import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from apps.diet_composer.models import Meal, DailyMenu

@pytest.mark.django_db
class TestMealView:
    @pytest.fixture(name="user", scope="class")
    def create_user(self, django_db_blocker, django_db_setup):
        with django_db_blocker.unblock():
            user = User.objects.create_user(
                username="test_user", email="test@demo.pl", password="test12345"
            )

        yield user
        with django_db_blocker.unblock():
            user.delete()

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

    def test_meal_create_view(self, client, menu):
        client.login(username="test_user", password="test12345")
        response = client.post(
            reverse("meal-create", kwargs={"pk": menu.id}),
            {
                "name": "Lunch"
            })
        assert response.status_code == 302
        assert menu.meals.count() == 1

    def test_meal_delete_view(self, client, menu):
        meal = Meal.objects.create(name="Lunch")
        meal.save()
        assert Meal.objects.count() == 1
        client.login(username="test_user", password="test12345")
        response = client.post(
            reverse("meal-delete", kwargs={"menu_id": menu.id, "pk": meal.id})
        )
        assert response.status_code == 302
        assert Meal.objects.count() == 0