from PIL import Image


def image_process(i):
    img = Image.open(i)
    pixels = list(img.getdata())
    res = 0
    for j in pixels[::10]:
        for color in j:
            res = (res + color) % 3
    return res + 1
