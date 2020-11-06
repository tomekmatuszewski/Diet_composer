import pytest
from django.contrib.auth.models import User
from apps.diet_composer.models import DailyMenu


@pytest.mark.django_db()
class TestDailyMenu:
    @pytest.fixture(name="menu", scope="class")
    def create_menu(self, django_db_blocker, django_db_setup):
        with django_db_blocker.unblock():
            user = User.objects.create_user(
                username="test_user", email="test@demo.pl", password="test12345"
            )
            daily_menu = DailyMenu(name="Test Menu", number_of_meals=3, author=user)
            daily_menu.save()
            daily_menu.meals.create(name="Test Meal")
        yield daily_menu
        with django_db_blocker.unblock():
            daily_menu.delete()
            user.delete()

    def test_menu_str(self, menu):
        assert str(menu) == "Daily Menu Test Menu created by test_user"

    def test_menu_calories(self, menu):
        assert menu.total_calories == 0

    def test_menu_proteins(self, menu):
        assert menu.total_proteins == 0

    def test_menu_fats(self, menu):
        assert menu.total_fats == 0

    def test_menu_carbohydrates(self, menu):
        assert menu.total_carbohydrates == 0
