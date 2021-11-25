from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from adminapp.forms import ShopUserAdminEditForm, ProductCategoryEditForm, ProductCategoryCreateForm, EditProductForm
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from mainapp.models import Product, ProductCategory


class AccessMixin:

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class AdminUserListView(AccessMixin, ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'
    extra_context = {'title': 'админка/пользователи'}

    def get_queryset(self):
        return ShopUser.objects.order_by('-is_active', '-is_superuser', '-is_staff', 'username')


# @user_passes_test(lambda u: u.is_superuser)
# def users(request):
#     title = 'админка/пользователи'
#
#     users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
#
#     context = {
#         'title': title,
#         'objects': users_list
#     }
#
#     return render(request, 'adminapp/users.html', context)


class AdminUserCreateView(AccessMixin, CreateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    form_class = ShopUserRegisterForm
    success_url = reverse_lazy('adminapp:users')
    extra_context = {'title': 'пользователи/создание'}


# @user_passes_test(lambda u: u.is_superuser)
# def user_create(request):
#     title = 'пользователи/создание'
#
#     if request.method == 'POST':
#         user_form = ShopUserRegisterForm(request.POST, request.FILES)
#         if user_form.is_valid():
#             user_form.save()
#             return HttpResponseRedirect(reverse('adminapp:users'))
#     else:
#         user_form = ShopUserRegisterForm()
#
#     context = {
#         'title': title,
#         'update_form': user_form,
#     }
#
#     return render(request, 'adminapp/user_update.html', context)


class AdminUserEditView(AccessMixin, UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    form_class = ShopUserAdminEditForm
    extra_context = {'title': 'пользователи/редактирование'}

    def get_success_url(self):
        return reverse('adminapp:user_update', args=[self.kwargs['pk']])


# @user_passes_test(lambda u: u.is_superuser)
# def user_update(request, pk):
#     title = 'пользователи/редактирование'
#
#     edit_user = get_object_or_404(ShopUser, pk=pk)
#     if request.method == 'POST':
#         edit_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)
#         if edit_form.is_valid():
#             edit_form.save()
#             return HttpResponseRedirect(reverse('adminapp:user_update', args=[edit_user.pk]))
#     else:
#         edit_form = ShopUserAdminEditForm(instance=edit_user)
#
#     context = {
#         'title': title,
#         'update_form': edit_form,
#     }
#
#     return render(request, 'adminapp/user_update.html', context)


class AdminUserDeleteView(AccessMixin, DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    extra_context = {'title': 'пользователи/удаление'}

    def delete(self, request, **kwargs):
        user = self.get_object()
        if user.is_active:
            user.is_active = False
        else:
            user.is_active = True
        user.save()
        return HttpResponseRedirect(reverse_lazy('adminapp:users'))


# @user_passes_test(lambda u: u.is_superuser)
# def user_delete(request, pk):
#     title = 'пользователи/удаление'
#
#     user = get_object_or_404(ShopUser, pk=pk)
#
#     if request.method == 'POST':
#         # user.delete()
#         # вместо удаления лучше сделаем неактивным
#         user.is_active = False
#         user.save()
#         return HttpResponseRedirect(reverse('adminapp:users'))
#
#     context = {
#         'title': title,
#         'user_to_delete': user,
#     }
#
#     return render(request, 'adminapp/user_delete.html', context)


class AdminCategoriesView(AccessMixin, ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'
    extra_context = {'title': 'админка/категории'}


# @user_passes_test(lambda u: u.is_superuser)
# def categories(request):
#     title = 'админка/категории'
#
#     categories_list = ProductCategory.objects.all()
#
#     context = {
#         'title': title,
#         'objects': categories_list
#     }
#
#     return render(request, 'adminapp/categories.html', context)


class AdminCategoryCreateView(AccessMixin, CreateView):
    model = ProductCategory
    template_name = 'adminapp/categories_create.html'
    form_class = ProductCategoryCreateForm
    success_url = reverse_lazy('adminapp:categories')
    extra_context = {'title': 'категории/создание'}


# @user_passes_test(lambda u: u.is_superuser)
# def category_create(request):
#     title = 'категории/создание'
#
#     if request.method == 'POST':
#         new_category_form = ProductCategoryCreateForm(request.POST)
#         if new_category_form.is_valid():
#             new_category_form.save()
#             return HttpResponseRedirect(reverse('adminapp:categories'))
#     else:
#         new_category_form = ProductCategoryCreateForm()
#
#     context = {
#         'title': title,
#         'category_create': new_category_form
#     }
#
#     return render(request, 'adminapp/categories_create.html', context)


class AdminCategoryUpdateView(AccessMixin, UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    form_class = ProductCategoryEditForm
    extra_context = {'title': 'категории/редактирование'}

    def get_success_url(self):
        return reverse('adminapp:category_update', args=[self.kwargs['pk']])


# @user_passes_test(lambda u: u.is_superuser)
# def category_update(request, pk):
#     title = 'категории/редактирование'
#
#     edit_category = get_object_or_404(ProductCategory, pk=pk)
#
#     if request.method == 'POST':
#         edit_category_form = ProductCategoryEditForm(request.POST, instance=edit_category)
#         if edit_category_form.is_valid():
#             edit_category_form.save()
#             return HttpResponseRedirect(reverse('adminapp:category_update', args=[edit_category.pk]))
#     else:
#         edit_category_form = ProductCategoryEditForm(instance=edit_category)
#
#     context = {
#         'title': title,
#         'category_update': edit_category_form
#     }
#
#     return render(request, 'adminapp/category_update.html', context)eRedirect(reverse_lazy('adminapp:users'))


class AdminCategoryDeleteView(AccessMixin, DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    extra_context = {'title': 'категории/удаление'}

    def delete(self, request, **kwargs):
        category = self.get_object()
        if category.is_active:
            category.is_active = False
        else:
            category.is_active = True
        category.save()
        return HttpResponseRedirect(reverse_lazy('adminapp:categories'))


# @user_passes_test(lambda u: u.is_superuser)
# def category_delete(request, pk):
#     title = 'категории/удаление'
#
#     category = get_object_or_404(ProductCategory, pk=pk)
#
#     if request.method == 'POST':
#         # user.delete()
#         # вместо удаления лучше сделаем неактивным
#         category.is_active = False
#         category.save()
#         return HttpResponseRedirect(reverse('adminapp:categories'))
#
#     context = {
#         'title': title,
#         'category_to_delete': category,
#     }
#
#     return render(request, 'adminapp/category_delete.html', context)


class AdminCategoryProductsView(AccessMixin, ListView):
    model = Product
    template_name = 'adminapp/products.html'
    extra_context = {'title': 'админка/продукты'}
    paginate_by = 2

    def get_queryset(self, **kwargs):
        return Product.objects.filter(category__pk=self.kwargs.get('pk')).order_by('-is_active', 'name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(ProductCategory, pk=self.kwargs.get('pk'))
        return context


# @user_passes_test(lambda u: u.is_superuser)
# def products(request, pk):
#     title = 'админка/продукты'
#
#     category = get_object_or_404(ProductCategory, pk=pk)
#     products_list = Product.objects.filter(category__pk=pk).order_by('name')
#
#     context = {
#         'title': title,
#         'category': category,
#         'objects': products_list,
#     }
#
#     return render(request, 'adminapp/products.html', context)


class AdminProductCreateView(AccessMixin, CreateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    form_class = EditProductForm
    extra_context = {'title': 'продукт/создание'}

    def get_success_url(self):
        return reverse('adminapp:products', args=[self.kwargs['pk']])

    def get_initial(self):
        initial = {'category': self.kwargs.get('pk')}
        return initial


# @user_passes_test(lambda u: u.is_superuser)
# def product_create(request, pk):
#     title = 'продукт/создание'
#     category = get_object_or_404(ProductCategory, pk=pk)
#
#     if request.method == 'POST':
#         product_form = EditProductForm(request.POST, request.FILES)
#         if product_form.is_valid():
#             product_form.save()
#             return HttpResponseRedirect(reverse('adminapp:products', args=[pk]))
#     else:
#         product_form = EditProductForm(initial={'category': category})
#
#     context = {'title': title,
#                'update_form': product_form,
#                'category': category
#                }
#
#     return render(request, 'adminapp/product_update.html', context)


class AdminProductView(AccessMixin, DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'
    extra_context = {'title': 'продукт/подробнее'}


# @user_passes_test(lambda u: u.is_superuser)
# def product_read(request, pk):
#     title = 'продукт/подробнее'
#     product = get_object_or_404(Product, pk=pk)
#     context = {
#         'title': title,
#         'object': product,
#     }
#
#     return render(request, 'adminapp/product_read.html', context)


class AdminProductUpdateView(AccessMixin, UpdateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    form_class = EditProductForm
    extra_context = {'title': 'продукт/редактирование'}

    def get_success_url(self):
        return reverse('adminapp:product_update', args=[self.kwargs['pk']])


# @user_passes_test(lambda u: u.is_superuser)
# def product_update(request, pk):
#     title = 'продукт/редактирование'
#
#     edit_product = get_object_or_404(Product, pk=pk)
#
#     if request.method == 'POST':
#         edit_form = EditProductForm(request.POST, request.FILES, instance=edit_product)
#         if edit_form.is_valid():
#             edit_form.save()
#             return HttpResponseRedirect(reverse('adminapp:product_update', args=[edit_product.pk]))
#     else:
#         edit_form = EditProductForm(instance=edit_product)
#
#     context = {'title': title,
#                'update_form': edit_form,
#                'category': edit_product.category
#                }
#
#     return render(request, 'adminapp/product_update.html', context)


class AdminProductDeleteView(AccessMixin, DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'
    extra_context = {'title': 'продукт/удаление'}

    def delete(self, request, **kwargs):
        product = self.get_object()
        if product.is_active:
            product.is_active = False
        else:
            product.is_active = True
        product.save()
        return HttpResponseRedirect(reverse('adminapp:products', args=[product.category.pk]))


# @user_passes_test(lambda u: u.is_superuser)
# def product_delete(request, pk):
#     title = 'продукт/удаление'
#
#     product = get_object_or_404(Product, pk=pk)
#
#     if request.method == 'POST':
#         product.is_active = False
#         product.save()
#         return HttpResponseRedirect(reverse('adminapp:products', args=[product.category.pk]))
#
#     context = {
#         'title': title,
#         'product_to_delete': product
#     }
#
#     return render(request, 'adminapp/product_delete.html', context)
