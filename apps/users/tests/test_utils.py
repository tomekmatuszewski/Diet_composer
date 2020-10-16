import os
from pathlib import Path

import pytest
from PIL import Image
from django.core.exceptions import ValidationError

from apps.users.utils import change_pic_size, validate_age, calculate_bmr, calculate_cmr, calc_daily_fats, calc_daily_proteins, calc_daily_carb

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent.parent


@pytest.fixture(scope="module", name="image_path")
def get_image():
    image_path = os.path.join(BASE_DIR, "media/test_pics/joker.jpg")
    yield image_path
    img = Image.open(image_path)
    img.thumbnail((400, 400))
    img.save(image_path)


def test_change_pic_size(image_path):
    change_pic_size(image_path, 300, 300)
    assert Image.open(image_path).height == 300
    assert Image.open(image_path).width == 300


def test_validate_age():
    assert validate_age(50)
    with pytest.raises(ValidationError):
        assert validate_age(120)

def test_calculate_bmr():
    assert calculate_bmr(80, 192, 25, "Male") == 1881.2
    assert calculate_bmr(60, 170, 25, "Female") == 1377.9

def test_calc_cmr():
    assert calculate_cmr(10, 2) == 20

def test_calc_daily_proteins_fats_carbo():
    assert calc_daily_proteins(1800) == 90
    assert calc_daily_fats(1800) == 50
    assert calc_daily_carb(1800) == 248


