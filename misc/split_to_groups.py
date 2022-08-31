import asyncio
from io import BytesIO

from PIL import Image

from loader import teachers


def image_process(i):
    img = Image.open(BytesIO(i))
    pixels = list(img.getdata())
    res = 0
    for j in pixels[::10]:
        for color in j:
            res = (res + color) % 3
    return res + 1

#
# async def main():
#     image = await teachers.get_photo(1998)
#     result = image_process(image)
#     print(result)
#
#
# asyncio.run(main())
