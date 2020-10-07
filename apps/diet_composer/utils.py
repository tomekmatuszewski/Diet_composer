def calculate_params(unit, value_to_calculate, weight, weight_in_psc) -> float:
    if unit == 'g':
        return round(float(value_to_calculate) * float(weight) / 100, 2)
    return round(float(value_to_calculate) * float(weight_in_psc) / 100 * weight, 2)