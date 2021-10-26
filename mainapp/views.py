from django.shortcuts import render
from mainapp.models import Product, ProductCategory


# Create your views here.

def main(request):
    context = {
        'title': 'главная',
        'products': Product.objects.all()[:4]
    }
    return render(request, 'mainapp/index.html', context=context)


def contact(request):
    context = {
        'title': 'контакты'
    }
    return render(request, 'mainapp/contact.html', context=context)


def products(request, pk=None):
    category = ProductCategory.objects.name

    context = {
        'links_menu': ProductCategory.objects.all(),
        'title': 'продукты'
    }
    return render(request, 'mainapp/products.html', context=context)
