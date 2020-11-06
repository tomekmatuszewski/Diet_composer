import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from apps.diet_composer.models import DailyMenu


@pytest.mark.django_db
class TestMenuView:
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

    def test_menu_create_view(self, client, menu):
        client.login(username="test_user", password="test12345")
        response = client.post(
            reverse("create-menu"),
            {
                "name": "Test Menu",
                "number_of_meals": 3
            })
        assert response.status_code == 302
        assert DailyMenu.objects.count() == 2

    def test_menu_detail_view(self, client, menu):
        client.login(username="test_user", password="test12345")
        response = client.get(
            reverse("menu-details", kwargs={"pk": menu.id})
        )
        assert response.status_code == 200

    def test_menu_update_view(self, client, menu, user):
        client.login(username="test_user", password="test12345")
        response = client.post(
            reverse("menu-update", kwargs={"username": user.username,
                                           "pk": menu.id}),
            data={
                "name": "Updated Test Menu",
                "number_of_meals": 5
            }
        )
        menu.refresh_from_db()
        assert response.status_code == 302
        assert menu.name == "Updated Test Menu"

    def test_user_menu_list_view(self, menu, user, client):
        client.login(username="test_user", password="test12345")
        response = client.get(
            reverse("user-menus", kwargs={"username": user.username})
        )
        assert response.status_code == 200


    def test_menu_delete_view(self, client, menu, user):
        client.login(username="test_user", password="test12345")
        response = client.post(
            reverse("menu-delete", kwargs={"username": user.username,
                                           "pk": menu.id})
        )
        assert response.status_code == 302



