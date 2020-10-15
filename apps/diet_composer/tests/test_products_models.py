import pytest
from django.contrib.auth.models import User

from apps.diet_composer.models import Product, ProductCategory, ProductItem


@pytest.mark.django_db()
class TestProduct:
    @pytest.fixture(name="product", scope="class")
    def create_product(self, django_db_blocker, django_db_setup):
        with django_db_blocker.unblock():
            user = User.objects.create_user(
                username="test_user", email="test@demo.pl", password="test12345"
            )
            category = ProductCategory.objects.create(name="Test Category")
            product = Product.objects.create(
                category=category, name="Test Product", calories_per_100=100,
                proteins_per_100=50, fats_per_100=50, carbohydrates_per_100=50,
                weight_of_pcs=100, author=user
            )
        yield product
        with django_db_blocker.unblock():
            product.delete()
            category.delete()
            user.delete()

    def test_product_name(self, product):
        assert str(product) == f"{product.name}, weight of piece/packege {product.weight_of_pcs} g"

    def test_product(self, product):
        assert product.name == "Test Product"
        assert product.author.username == "test_user"
        assert product.category.name == "Test Category"


@pytest.mark.django_db()
class TestProductItem:
    @pytest.fixture(name="product_item", scope="class")
    def create_productitem(self, django_db_blocker, django_db_setup):
        with django_db_blocker.unblock():
            user = User.objects.create_user(
                username="test_user1", email="test1@demo.pl", password="test12345"
            )
            category = ProductCategory.objects.create(name="Test Category2")
            product = Product.objects.create(
                category=category, name="Test Product", calories_per_100=100,
                proteins_per_100=50, fats_per_100=50, carbohydrates_per_100=50,
                weight_of_pcs=100, author=user
            )
            product_item = ProductItem(product=product, category=category,
                                       unit="g", weight=150)
        yield product_item
        with django_db_blocker.unblock():
            product.delete()
            category.delete()
            user.delete()

    def test_product_item_name(self, product_item):
        assert str(product_item) == f"Ingredient: {product_item.product.name}, {product_item.weight_of_pcs} g"

    def test_product_calories(self, product_item):
        assert product_item.calories == 150

    def test_product_weight_of_pcs(self, product_item):
        assert product_item.weight_of_pcs == 150

    def test_product_proteins(self, product_item):
        assert product_item.proteins == 75

    def test_product_fats(self, product_item):
        assert product_item.fats == 75

    def test_product_carbohydrates(self, product_item):
        assert product_item.carbohydrates == 75

    def test_product_weight_piece(self, product_item):
        product_item.unit = "piece"
        product_item.weight = 1
        assert product_item.weight_of_pcs == 100