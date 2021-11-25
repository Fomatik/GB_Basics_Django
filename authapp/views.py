from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import CreateView, UpdateView

from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm
from django.contrib import auth
from django.urls import reverse, reverse_lazy

from authapp.models import ShopUser


class UserLoginView(LoginView):
    template_name = 'authapp/login.html'
    authentication_form = ShopUserLoginForm
    success_url = 'main'
    extra_context = {'title': 'вход'}


# def login(request):
#     title = 'вход'
#
#     login_form = ShopUserLoginForm(data=request.POST)
#
#     next_param = request.GET.get('next', '')
#     print(next_param)
#
#     if request.method == 'POST' and login_form.is_valid():
#         username = request.POST['username']
#         password = request.POST['password']
#
#         user = auth.authenticate(username=username, password=password)
#         if user and user.is_active:
#             auth.login(request, user)
#             if 'next' in request.POST.keys():
#                 return HttpResponseRedirect(request.POST['next'])
#             return HttpResponseRedirect(reverse('main'))
#
#     context = {
#         'title': title,
#         'login_form': login_form,
#         'next': next_param,
#     }
#     return render(request, 'authapp/login.html', context)


class UserLogoutView(LogoutView):
    pass


# def logout(request):
#     auth.logout(request)
#     return HttpResponseRedirect(reverse('main'))


class UserRegisterView(SuccessMessageMixin, CreateView):
    template_name = 'authapp/register.html'
    success_url = reverse_lazy('auth:login')
    form_class = ShopUserRegisterForm
    success_message = "Your profile was created successfully"
    extra_context = {'title': 'регистрация'}


# def register(request):
#     title = 'регистрация'
#
#     if request.method == 'POST':
#         register_form = ShopUserRegisterForm(request.POST, request.FILES)
#
#         if register_form.is_valid():
#             register_form.save()
#             return HttpResponseRedirect(reverse('auth:login'))
#     else:
#         register_form = ShopUserRegisterForm()
#
#     context = {'title': title, 'register_form': register_form}
#
#     return render(request, 'authapp/register.html', context)


class UserProfileEditView(UpdateView):
    model = ShopUser
    template_name = 'authapp/edit.html'
    success_url = reverse_lazy('auth:edit')
    form_class = ShopUserEditForm
    extra_context = {'title': 'редактирование'}

    def get_object(self, queryset=None):
        return self.request.user


# def edit(request):
#     title = 'редактирование'
#
#     if request.method == 'POST':
#         edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
#         if edit_form.is_valid():
#             edit_form.save()
#             return HttpResponseRedirect(reverse('auth:edit'))
#     else:
#         edit_form = ShopUserEditForm(instance=request.user)
#
#     context = {'title': title, 'edit_form': edit_form}
#
#     return render(request, 'authapp/edit.html', context)
