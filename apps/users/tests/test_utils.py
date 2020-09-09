import os
from pathlib import Path

import pytest
from PIL import Image

from apps.users.utils import change_pic_size

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent.parent


@pytest.fixture(scope="module", name="image_path")
def get_image():
    image_path = os.path.join(BASE_DIR, "media/test_pics/joker.jpg")
    yield image_path
    img = Image.open(image_path)
    img.thumbnail((400, 400))
    img.save(image_path)


def test_change_pic_size(image_path):
    change_pic_size(image_path)
    assert Image.open(image_path).height == 300
    assert Image.open(image_path).width == 300
