from django.core.management.base import BaseCommand
from mainapp.models import Product, ProductCategory
from authapp.models import ShopUser
from django.conf import settings

import json

JSON_PATH = 'mainapp/json'


def load_db_from_json(filename):
    with open(f'{settings.BASE_DIR}/{JSON_PATH}/{filename}.json', 'r', encoding='utf-8') as json_file:
        return json.load(json_file)


class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = load_db_from_json('categories')

        ProductCategory.objects.all().delete()
        for category in categories:
            ProductCategory.objects.create(**category)

        products = load_db_from_json('products')

        Product.objects.all().delete()
        for product in products:
            category_name = product['category']
            product['category'] = ProductCategory.objects.get(name=category_name)
            Product.objects.create(**product)

        ShopUser.objects.all().delete()

        super_user = ShopUser.objects.create_superuser('django', 'django@geekshop.local', 'geekbrains', age=33, first_name='Django')