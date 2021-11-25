from django import template
from django.conf import settings


register = template.Library()


@register.filter(name='product_img')
def product_img(img_path):
    if img_path is None or not img_path:
        img_path = 'products_images/default.png'
    return f'{settings.MEDIA_URL}{img_path}'


@register.filter(name='user_img')
def user_img(img_path):
    if img_path is None or not img_path:
        img_path = 'user_avatars/default.png'
    return f'{settings.MEDIA_URL}{img_path}'