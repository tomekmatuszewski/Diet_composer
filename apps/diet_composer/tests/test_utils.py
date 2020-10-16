import pytest
from unittest.mock import MagicMock
from decimal import Decimal
from apps.diet_composer.utils import (
    calculate_params,
    check_nutritional_status,
    calculate_total_value_menu,
    calculate_total_value_meal,
    calculate_recipe_nutri,
    calculate_weight,
)


def test_calculate_params():
    unit1 = "g"
    unit2 = "piece"
    value_to_calc = Decimal(10.5)
    weight1 = Decimal(50)
    weight2 = Decimal(2)
    weight_in_pcs = Decimal(100)
    assert calculate_params(unit1, value_to_calc, weight1, weight_in_pcs) == 5.25
    assert calculate_params(unit2, value_to_calc, weight2, weight_in_pcs) == 21


@pytest.fixture(name="menu", scope="function")
def create_menu():
    menu = MagicMock(total_calories=100, total_proteins=20, total_fats=10, total_carbohydrates=10)
    return menu


@pytest.fixture(name="ingredient", scope="function")
def create_ingredient():
    ingredient = MagicMock(calories=100, proteins=20, fats=10, carbohydrates=10)
    return ingredient


@pytest.fixture(name="user1", scope="function")
def create_user1():
    attrs = {'profile.cmr': 1000,
             'profile.daily_proteins': 80,
             'profile.daily_fats': 80,
             'profile.daily_carb': 80,
             }
    user1 = MagicMock(**attrs)
    return user1

@pytest.fixture(name="user2", scope="function")
def create_user2():
    attrs = {'profile.cmr': 100,
             'profile.daily_proteins': 50,
             'profile.daily_fats': 50,
             'profile.daily_carb': 80,
             }
    user2 = MagicMock(**attrs)
    return user2


def test_check_nutritional_status(menu, ingredient, user1, user2):
    assert check_nutritional_status(user1, menu, ingredient)
    assert not check_nutritional_status(user2, menu, ingredient)


def test_total_value_menu():
    meal1 = MagicMock(total_calories=100, total_proteins=10, total_fats=5, total_carbohydrates=13)
    meal2 = MagicMock(total_calories=98, total_proteins=20, total_fats=6, total_carbohydrates=5)
    lst_meals = [meal1, meal2]
    assert calculate_total_value_menu(lst_meals, "calories") == 198
    assert calculate_total_value_menu(lst_meals, "proteins") == 30
    assert calculate_total_value_menu(lst_meals, "fats") == 11
    assert calculate_total_value_menu(lst_meals, "carbohydrates") == 18


def test_calculate_total_value_meal():
    ingredient1 = MagicMock(calories=10, proteins=5, fats=8, carbohydrates=6)
    ingredient2 = MagicMock(calories=10, proteins=5, fats=8, carbohydrates=6)
    recipe1 = MagicMock(calories=100, proteins=15, fats=20, carbohydrates=80)
    lst_ingredients = [ingredient1, ingredient2]
    lst_recipes = [recipe1]
    assert calculate_total_value_meal(lst_ingredients, lst_recipes, "calories") == 120
    assert calculate_total_value_meal(lst_ingredients, lst_recipes, "proteins") == 25
    assert calculate_total_value_meal(lst_ingredients, lst_recipes, "fats") == 36
    assert calculate_total_value_meal(lst_ingredients, lst_recipes, "carbohydrates") == 92


def test_calc_recipe_nutri():
    calories = Decimal(100.25)
    piece = Decimal(1.5)
    assert calculate_recipe_nutri(calories, piece) == 150.38


def test_calc_weight():
    unit1 = "g"
    unit2 = "piece"
    weight1 = Decimal(15)
    weight2 = Decimal(1)
    weight_pcs = Decimal(100)
    assert calculate_weight(unit1, weight1, weight_pcs) == 15
    assert calculate_weight(unit2, weight2, weight_pcs) == 100
