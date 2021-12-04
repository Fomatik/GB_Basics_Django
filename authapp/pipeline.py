from datetime import datetime

import requests
from django.conf import settings
from social_core.exceptions import AuthForbidden

from authapp.models import ShopUserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    url_method = 'https://api.vk.com/method/'
    access_token = response.get('access_token')
    fields = ','.join(['bdate', 'sex', 'about'])

    users_api_url = f'{url_method}users.get?fields={fields}&access_token={access_token}&v=5.131'
    photos_api_url = f'{url_method}photos.get?album_id=profile&access_token={access_token}&v=5.131'

    user_response = requests.get(users_api_url)
    photos_response = requests.get(photos_api_url)

    if user_response.status_code != 200:
        return

    # print(response.json())
    users_data_json = user_response.json()['response'][0]
    photo_data_json = photos_response.json()['response']['items'][-1]['sizes'][-1]

    if 'sex' in users_data_json:
        if users_data_json['sex'] == 1:
            user.shopuserprofile.gender = ShopUserProfile.FEMALE
        elif users_data_json['sex'] == 2:
            user.shopuserprofile.gender = ShopUserProfile.MALE
        else:
            user.shopuserprofile.gender = ShopUserProfile.OTHERS

    if 'bdate' in users_data_json:
        birthday = datetime.strptime(users_data_json['bdate'], '%d.%m.%Y')

        age = datetime.now().year - birthday.year
        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')

        user.age = age

    if 'about' in users_data_json:
        user.shopuserprofile.about = users_data_json['about']

    if 'url' in photo_data_json:
        photo_path = f'/user_avatars/{user.pk}.jpg'
        photo_full_path = f'{settings.MEDIA_ROOT}{photo_path}'
        photo_data = requests.get(photo_data_json['url'])
        with open(photo_full_path, 'wb') as photo_file:
            photo_file.write(photo_data.content)
        user.avatar = photo_path

    user.save()
