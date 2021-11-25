import random

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, TemplateView, DetailView

from basketapp.models import Basket
from mainapp.models import Product, ProductCategory


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    else:
        return []


def get_hot_product():
    hot_products = Product.objects.all()
    return random.sample(list(hot_products), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]
    return same_products


class MainView(ListView):
    model = Product
    template_name = 'mainapp/index.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.all().order_by('?')[:4]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['basket'] = get_basket(self.request.user)
        context['title'] = 'Главная'
        return context


# def main(request):
#     context = {
#         'title': 'главная',
#         'products': Product.objects.all().order_by('?')[:4],
#         'basket': get_basket(request.user),
#     }
#     return render(request, 'mainapp/index.html', context=context)


class ContactView(TemplateView):
    template_name = 'mainapp/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Контакты'
        context['basket'] = get_basket(self.request.user)
        return context


# def contact(request):
#     context = {
#         'title': 'контакты',
#         'basket': get_basket(request.user),
#     }
#     return render(request, 'mainapp/contact.html', context=context)


class ProductsView(ListView):
    model = Product
    template_name = 'mainapp/products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Продукты'
        context['links_menu'] = ProductCategory.objects.all()
        context['hot_products'] = get_hot_product()
        context['same_products'] = get_same_products(get_hot_product())
        context['basket'] = get_basket(self.request.user)
        return context


class ProductsFromCategoryView(ListView):
    paginate_by = 2
    template_name = 'mainapp/products_list.html'

    def get_queryset(self, **kwargs):
        if self.kwargs['pk'] == 0:
            return Product.objects.all().order_by('-id')
        else:
            return Product.objects.filter(category__id=self.kwargs['pk']).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(ProductCategory, pk=self.kwargs['pk']) if self.kwargs['pk'] > 0 else {'name': 'все', 'pk': 0}
        context['title'] = context['category']
        context['links_menu'] = ProductCategory.objects.all()
        context['products'] = self.get_queryset()
        context['basket'] = get_basket(self.request.user)
        return context

# def products(request, pk=None):
#
#     links_menu = ProductCategory.objects.all()
#     title = 'продукты'
#     basket = get_basket(request.user)
#
#     if pk is not None:
#         if pk == 0:
#             products_list = Product.objects.all()
#             category_item = {
#                 'name': 'все',
#                 'pk': 0,
#             }
#         else:
#             category_item = get_object_or_404(ProductCategory, pk=pk)
#             products_list = Product.objects.filter(category__pk=pk)
#
#         paginator = Paginator(products_list, 3)
#         page = request.GET.get('page', 1)
#         try:
#             page_obj = paginator.page(page)
#         except PageNotAnInteger:
#             page_obj = paginator.page(1)
#         except EmptyPage:
#             page_obj = paginator.page(paginator.num_pages)
#
#         context = {
#             'links_menu': links_menu,
#             'title': title,
#             'category': category_item,
#             'products': page_obj,
#             'basket': basket,
#         }
#
#         return render(request, 'mainapp/products_list.html', context=context)
#
#     hot_products = get_hot_product()
#     same_products = get_same_products(hot_products)
#
#     context = {
#         'title': title,
#         'links_menu': links_menu,
#         'hot_products': hot_products,
#         'same_products': same_products,
#         'basket': basket,
#     }
#
#     return render(request, 'mainapp/products.html', context=context)


class ProductView(DetailView):
    model = Product
    template_name = 'mainapp/product.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Product.name
        context['links_menu'] = ProductCategory.objects.all()
        context['product'] = Product.objects.all().filter(pk=self.kwargs['pk'])
        context['basket'] = get_basket(self.request.user)
        return context


# def product(request, pk):
#     title = 'продукты'
# 
#     content = {
#         'title': title,
#         'links_menu': ProductCategory.objects.all(),
#         'product': get_object_or_404(Product, pk=pk),
#         'basket': get_basket(request.user),
#     }
# 
#     return render(request, 'mainapp/product.html', content)
