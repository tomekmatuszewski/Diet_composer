from apps.diet_composer import forms
import pytest
from apps.diet_composer.models import Product, ProductCategory
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestForms:

    @pytest.fixture(scope="function", name="product")
    def create_product(self, django_db_blocker, django_db_setup, user):
        category = ProductCategory.objects.create(name="cat1")
        product = Product.objects.create(category=category, name="prod1", calories_per_100=100, proteins_per_100=100,
                                         fats_per_100=100, carbohydrates_per_100=100, author=user)
        yield product
        with django_db_blocker.unblock():
            product.delete()
            category.delete()

    @pytest.fixture(scope="class", name="user")
    def create_user(self, django_db_blocker, django_db_setup):
        with django_db_blocker.unblock():
            user = User.objects.create(username="user1", password="pass123")
            yield user
        with django_db_blocker.unblock():
            user.delete()

    def test_product_item_valid_data(self, product):
        form = forms.ProductItemForm(
            data={
                "category": product.category.id,
                "product": product.id,
                "weight": 100,
                "unit": "g",
            }
        )
        assert form.is_valid()

    def test_product_form(self, user):
        category = ProductCategory.objects.create(name="cat2")
        form = forms.ProductForm(
            data={
                "category": category,
                "name": "test_product",
                "calories_per_100": 100,
                "proteins_per_100": 50,
                "fats_per_100": 10,
                "carbohydrates_per_100": 80,
                "author": user
            }
        )
        assert form.is_valid()