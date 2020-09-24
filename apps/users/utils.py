from PIL import Image


def change_pic_size(path, size1, size2) -> None:
    img = Image.open(path)
    if img.height > size1 or img.width > size2:
        output_size = (size1, size2)
        img.thumbnail(output_size)
        img.save(path)
