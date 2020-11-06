import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from apps.diet_composer.models import Product, ProductCategory, ProductItem, Meal, DailyMenu
from apps.users.models import UserActivity


@pytest.mark.django_db
class TestProductItemView:
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

    @pytest.fixture(name="product", scope="class")
    def create_product(self, django_db_blocker, django_db_setup, user):
        with django_db_blocker.unblock():
            category = ProductCategory.objects.create(name="cat1")
            category.save()
            product = Product.objects.create(
                category=category,
                name="product_testing",
                calories_per_100=80,
                proteins_per_100=50,
                fats_per_100=10,
                carbohydrates_per_100=80,
                weight_of_pcs=150,
                author=user
            )
            product.save()
        yield product
        with django_db_blocker.unblock():
            product.delete()
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

    def test_create_update_product_item(self, client, product, user, menu, meal):
        client.login(username="test_user", password="test12345")
        response = client.post(reverse("ingredient-create", kwargs={"menu_id": menu.id, "meal_id": meal.id}),
                               data={
                                   "category": product.category.id,
                                   "product": product.id,
                                   "weight": 1,
                               })
        assert response.status_code == 302
        assert ProductItem.objects.count() == 1

        id_ = ProductItem.objects.first().id

        response = client.post(reverse("ingredient-edit", kwargs={"menu_id": menu.id, "pk": id_}),
                               data={
                                   "category": product.category.id,
                                   "product": product.id,
                                   "weight": 100,
                                   "unit": "g"
                               })
        assert response.status_code == 302
        assert ProductItem.objects.first().weight == 100
        assert ProductItem.objects.first().unit == "g"

    def test_delete_product_item(self, client, product, user, menu, meal):
        client.login(username="test_user", password="test12345")
        response = client.post(reverse("ingredient-create", kwargs={"menu_id": menu.id, "meal_id": meal.id}),
                               data={
                                   "category": product.category.id,
                                   "product": product.id,
                                   "weight": 1,
                               })
        assert response.status_code == 302
        assert ProductItem.objects.count() == 1

        id_ = ProductItem.objects.first().id

        response = client.post(reverse("ingredient-delete", kwargs={"menu_id": menu.id, "pk": id_}))
        assert response.status_code == 302
        assert ProductItem.objects.count() == 0