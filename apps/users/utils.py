from PIL import Image
from django.core.exceptions import ValidationError


def change_pic_size(path, size1, size2) -> None:
    img = Image.open(path)
    if img.height > size1 or img.width > size2:
        output_size = (size1, size2)
        img.thumbnail(output_size)
        img.save(path)


def validate_age(value):
    if value > 110:
        raise ValidationError(f'Enter correct age value')


def calculate_bmr(weight, height, age, gender) -> float:
    if gender == "Male":
        return round((9.99 * weight + 6.25 * height - 4.92 * age + 5), 2)
    elif gender == "Female":
        return round((9.99 * weight + 6.25 * height - 4.92 * age - 161), 2)


def calculate_cmr(bmr, activity) -> float:
    return round(bmr * activity, 0)


def calc_daily_proteins(cmr) -> float:
    FACTOR = 0.2
    CALORIES_PER_GRAM = 4
    return round((cmr * FACTOR) / CALORIES_PER_GRAM, 0)


def calc_daily_fats(cmr) -> float:
    FACTOR = 0.25
    CALORIES_PER_GRAM = 9
    return round((cmr * FACTOR) / CALORIES_PER_GRAM, 0)


def calc_daily_carb(cmr) -> float:
    FACTOR = 0.55
    CALORIES_PER_GRAM = 4
    return round((cmr * FACTOR) / CALORIES_PER_GRAM, 0)
