import pytest
from unittest.mock import MagicMock
from django.urls import reverse, resolve

from apps.diet_composer.views import UserMenuListView, ProductCreateView, ProductListView, ProductUpdateView, \
    ProductDeleteView, MenuCreateView, MenuDetailView, MenuUpdateView, MenuDeleteView, ProductItemUpdateView, \
    ProductItemCreateView, ProductItemDeleteView, load_products, load_recipes, MealCreateView, RecipeItemCreateView, \
    RecipeItemUpdateView, RecipeItemDeleteView


@pytest.fixture(scope="function", name="user")
def crate_user():
    user = MagicMock(id=1, username="tm")
    return user


@pytest.fixture(scope="function", name="product")
def crate_product():
    product = MagicMock(id=1)
    return product


@pytest.fixture(scope="function", name="menu")
def crate_menu():
    menu = MagicMock(id=1)
    return menu


@pytest.fixture(scope="function", name="meal")
def crate_meal():
    meal = MagicMock(id=1)
    return meal

@pytest.fixture(scope="function", name="recipe_item")
def crate_recipe():
    recipe = MagicMock(id=1)
    return recipe

def test_menu_list_url(user):
    url = reverse("user-menus", kwargs={"username": user.username})
    assert resolve(url).func.view_class == UserMenuListView


def test_new_product_url(user):
    url = reverse("product-create")
    assert resolve(url).func.view_class == ProductCreateView


def test_products_list_url(user):
    url = reverse("products-list", kwargs={"username": user.username})
    assert resolve(url).func.view_class == ProductListView


def test_product_update_url(product):
    url = reverse("product-update", kwargs={"pk": product.id})
    assert resolve(url).func.view_class == ProductUpdateView


def test_product_delete_url(product):
    url = reverse("product-delete", kwargs={"pk": product.id})
    assert resolve(url).func.view_class == ProductDeleteView


def test_menu_create_url():
    url = reverse("create-menu")
    assert resolve(url).func.view_class == MenuCreateView


def test_menu_detail_url(menu):
    url = reverse("menu-details", kwargs={"pk": menu.id})
    assert resolve(url).func.view_class == MenuDetailView


def test_menu_update_view(menu, user):
    url = reverse("menu-update", kwargs={"username": user.id, "pk": menu.id})
    assert resolve(url).func.view_class == MenuUpdateView


def test_menu_delete_view(menu, user):
    url = reverse("menu-delete", kwargs={"username": user.id, "pk": menu.id})
    assert resolve(url).func.view_class == MenuDeleteView


def test_ingredient_create_view(menu, meal):
    url = reverse("ingredient-create", kwargs={"menu_id": menu.id, "meal_id": meal.id})
    assert resolve(url).func.view_class == ProductItemCreateView


def test_ingredient_update_view(menu, product):
    url = reverse("ingredient-edit", kwargs={"menu_id": menu.id, "pk": product.id})
    assert resolve(url).func.view_class == ProductItemUpdateView


def test_ingredient_delete_view(menu, product):
    url = reverse("ingredient-delete", kwargs={"menu_id": menu.id, "pk": product.id})
    assert resolve(url).func.view_class == ProductItemDeleteView


def test_ajax_load_products():
    url = reverse("ajax-load-products")
    assert resolve(url).func == load_products


def test_ajax_load_recipes():
    url = reverse("ajax-load-recipes")
    assert resolve(url).func == load_recipes


def test_create_meal_url(meal):
    url = reverse("meal-create", kwargs={"pk": meal.id})
    assert resolve(url).func.view_class == MealCreateView


def test_create_recipe_item(menu, meal):
    url = reverse("recipeitem-create", kwargs={"menu_id": menu.id, "meal_id": meal.id})
    assert resolve(url).func.view_class == RecipeItemCreateView


def test_recipe_item_update_url(menu, recipe_item):
    url = reverse("recipeitem-edit", kwargs={"menu_id": menu.id,"pk": recipe_item.id})
    assert resolve(url).func.view_class == RecipeItemUpdateView


def test_recipe_item_delete_url(menu, recipe_item):
    url = reverse("recipeitem-delete", kwargs={"menu_id": menu.id,"pk": recipe_item.id})
    assert resolve(url).func.view_class == RecipeItemDeleteView