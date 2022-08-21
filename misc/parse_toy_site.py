import requests
from io import BytesIO

URL_TEMPLATE = "https://teacherofrussia.ru/api/competitors?year=2022"


async def get_teachers_list() -> list[dict]:
    r = requests.get(URL_TEMPLATE)
    teachers_list = []
    for user in r.json():
        photo = requests.get(user['avatar']['file_path'])
        teacher: dict = {'id': user['id'],
                         'region': user['region']['name'],
                         'full_name': user['user']['full_name'],
                         'photo': BytesIO(photo.content)}
        teachers_list.append(teacher)
    return teachers_list
