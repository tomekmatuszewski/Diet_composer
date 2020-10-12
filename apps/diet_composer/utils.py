def calculate_params(unit, value_to_calculate, weight, weight_in_psc) -> float:
    if unit == 'g':
        return round(float(value_to_calculate) * float(weight) / 100, 2)
    return round(float(value_to_calculate) * float(weight_in_psc) / 100 * float(weight), 2)


def check_nutritional_status(user, menu, ingredient) -> bool:
    calories = menu.total_calories + ingredient.calories
    proteins = menu.total_proteins + ingredient.proteins
    fats = menu.total_fats + ingredient.fats
    carbohydrates = menu.total_carbohydrates + ingredient.carbohydrates

    if calories > user.profile.cmr or proteins > user.profile.daily_proteins or \
            fats > user.profile.daily_fats or carbohydrates > user.profile.daily_carb:
        return False
    return True
