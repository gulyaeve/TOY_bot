import io

from PIL import Image


def list_of_images_classificator(imglist: list[io.BytesIO]) -> list:
    temp = []
    ans = []
    for num, i in enumerate(imglist):
        img = Image.open(i)
        pixels = list(img.getdata())
        res = 0
        for j in pixels[::10]:
            for color in j:
                res += color
        temp.append((num, res))
    temp.sort(key=lambda x: x[1])
    for i in range(15):
        ans.append(temp[i][0])
    return ans
