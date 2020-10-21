import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from apps.diet_composer.models import Product, ProductCategory


@pytest.mark.django_db
class TestProductView:
    @pytest.fixture(name="user", scope="class")
    def create_user(self, django_db_blocker, django_db_setup):
        with django_db_blocker.unblock():
            user = User.objects.create_user(
                username="test_user", email="test@demo.pl", password="test12345"
            )

        yield user
        with django_db_blocker.unblock():
            user.delete()

    @pytest.fixture(name="product", scope="class")
    def create_product(self, django_db_blocker, django_db_setup, user):
        with django_db_blocker.unblock():
            category = ProductCategory.objects.create(name="cat1")
            product = Product.objects.create(
                category=category,
                name="product_testing",
                calories_per_100=100,
                proteins_per_100=50,
                fats_per_100=50,
                carbohydrates_per_100=50,
                weight_of_pcs=100,
                author=user
            )
        yield product
        with django_db_blocker.unblock():
            product.delete()
            category.delete()

    def test_product_create_view(self, client, product):
        client.login(username="test_user", password="test12345")
        response = client.post(
            reverse("product-create"),
            data={
                "category": product.category.id,
                "name": "added_product",
                "calories_per_100": 100,
                "proteins_per_100": 40,
                "fats_per_100": 10,
                "carbohydrates_per_100": 80
            },
        )
        assert response.status_code == 302
        assert Product.objects.count() == 2
        assert Product.objects.get(name="added_product")

    def test_products_list_view(self, client, user):
        client.login(username="test_user", password="test12345")
        response = client.get(reverse("products-list", args=[user.username]))
        assert response.status_code == 200
        assert response.context[0]["products"].count() == 1

    def test_product_update_view(self, client, user, product):
        client.login(username="test_user", password="test12345")
        response = client.post(
            reverse("product-update", args=[product.pk]),
            data={
                "category": product.category.id,
                "name": "added_product_updated",
                "calories_per_100": 200,
                "proteins_per_100": 40,
                "fats_per_100": 10,
                "carbohydrates_per_100": 80
            }
        )
        assert response.status_code == 302
        assert Product.objects.get(name="added_product_updated")
        assert Product.objects.get(name="added_product_updated").calories_per_100 == 200

    def test_product_delete_view(self, client, product):
        client.login(username="test_user", password="test12345")
        response = client.post(reverse("product-delete", args=[product.pk]))
        assert response.status_code == 302
        assert Product.objects.count() == 0





