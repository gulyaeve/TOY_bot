import requests

URL_TEMPLATE = "https://teacherofrussia.ru/api/competitors?year=2022"
# URL_TEMPLATE = "https://teacherofrussia.ru/api/competition?year=2022"


def get_teachers_list() -> list[dict]:
    r = requests.get(URL_TEMPLATE)
    teachers_list = []
    for user in r.json():
        photo = requests.get(user['avatar']['file_path'])
        teacher: dict = {'id': int(user['id']),
                         'full_name': f"{user['user']['last_name']} {user['user']['first_name']} {user['user']['father_name']}",
                         'region': user['region']['name'],
                         'subject': [d['name'] for d in user['subject']],
                         'photo_raw_file': photo.content}
        teachers_list.append(teacher)
    return teachers_list


# get_teachers_list()
