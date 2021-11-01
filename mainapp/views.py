import random
from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from mainapp.models import Product, ProductCategory


def get_basket(user):
    if user.is_authenticated:
        return sum(list(Basket.objects.filter(user=user).values_list('quantity', flat=True)))
    return 0


def main(request):
    context = {
        'title': 'главная',
        'products': Product.objects.all().order_by('?')[:4],
        'basket': get_basket(request.user),
    }
    return render(request, 'mainapp/index.html', context=context)


def contact(request):
    context = {
        'title': 'контакты',
        'basket': get_basket(request.user),
    }
    return render(request, 'mainapp/contact.html', context=context)


def products(request, pk=None):

    links_menu = ProductCategory.objects.all()
    title = 'продукты'

    if pk is not None:
        if pk == 0:
            products_list = Product.objects.all()
            category_item = {
                'name': 'все',
                'pk': 0,
            }
        else:
            category_item = get_object_or_404(ProductCategory, pk=pk)
            products_list = Product.objects.filter(category__pk=pk)

        context = {
            'links_menu': links_menu,
            'title': title,
            'category': category_item,
            'products': products_list,
            'basket': get_basket(request.user),
        }

        return render(request, 'mainapp/products_list.html', context=context)

    hot_products = random.sample(list(Product.objects.all()), 1)[0]
    same_products = Product.objects.all()[3:6]

    context = {
        'title': title,
        'links_menu': links_menu,
        'hot_products': hot_products,
        'same_products': same_products,
        'basket': get_basket(request.user),
    }

    return render(request, 'mainapp/products.html', context=context)
