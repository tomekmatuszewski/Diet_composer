from django.contrib.auth.models import User
from typing import TypeVar, List
from decimal import Decimal

DailyMenu = TypeVar("DailyMenu")
ProductItem = TypeVar("ProductItem")
RecipeItem = TypeVar("RecipeItem")
Meal = TypeVar("Meal")


def calculate_params(
    unit: str, value_to_calculate: Decimal, weight: Decimal, weight_in_psc: Decimal
) -> float:
    if unit == "g":
        return round(float(value_to_calculate) * float(weight) / 100, 2)
    return round(
        float(value_to_calculate) * float(weight_in_psc) / 100 * float(weight), 2
    )


def check_nutritional_status(
    user: User, menu: DailyMenu, ingredient: ProductItem
) -> bool:
    """ "
    checking personal parameters of user vs diet values
    """
    calories = menu.total_calories + ingredient.calories
    proteins = menu.total_proteins + ingredient.proteins
    fats = menu.total_fats + ingredient.fats
    carbohydrates = menu.total_carbohydrates + ingredient.carbohydrates

    if (
        calories > user.profile.cmr
        or proteins > user.profile.daily_proteins
        or fats > user.profile.daily_fats
        or carbohydrates > user.profile.daily_carb
    ):
        return False
    return True


def calculate_total_value_menu(lst: List[Meal], flag: str) -> float:
    total = 0
    for item in lst:
        if flag == "calories":
            total += item.total_calories
        elif flag == "proteins":
            total += item.total_proteins
        elif flag == "fats":
            total += item.total_fats
        else:
            total += item.total_carbohydrates
    return round(total, 2)


def calculate_total_value_meal(
    lst_ingredients: List[ProductItem], lst_recipes: List[RecipeItem], flag: str
) -> float:
    total = 0
    total_items = list(lst_ingredients) + list(lst_recipes)
    for item in total_items:
        if flag == "calories":
            total += item.calories
        elif flag == "proteins":
            total += item.proteins
        elif flag == "fats":
            total += item.fats
        else:
            total += item.carbohydrates
    return round(total, 2)


def calculate_recipe_nutri(nutri_value: Decimal, piece: Decimal) -> float:
    return round(float(nutri_value) * float(piece), 2)


def calculate_weight(unit: str, weight: Decimal, weight_pcs: Decimal) -> float:
    if unit == "g":
        return float(weight)
    return round(float(weight_pcs * weight), 1)
