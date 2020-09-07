from PIL import Image


def change_pic_size(path) -> None:
    img = Image.open(path)
    if img.height > 300 or img.width > 300:
        output_size = (300, 300)
        img.thumbnail(output_size)
        img.save(path)