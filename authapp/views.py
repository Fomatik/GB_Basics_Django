from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import CreateView, UpdateView

from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm, ShopUserProfileEditForm
from django.contrib import auth
from django.urls import reverse, reverse_lazy

from authapp.models import ShopUser, ShopUserProfile
from authapp.services import send_verify_email


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

    def form_valid(self, form):
        new_user = form.save()
        send_verify_email(new_user)
        return super(UserRegisterView, self).form_valid(form)


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
    template_name = 'authapp/edit.html'
    user_form_class = ShopUserEditForm
    profile_form_class = ShopUserProfileEditForm

    def get(self, request, **kwargs):
        user_form = self.user_form_class(instance=request.user)
        profile_form = self.profile_form_class(instance=request.user.shopuserprofile)
        return render(request, self.template_name, {'user_form': user_form, 'profile_form': profile_form, 'title': 'редактирование'})

    def post(self, request, **kwargs):
        if request.method == 'POST':
            user_form = self.user_form_class(request.POST, request.FILES, instance=request.user)
            profile_form = self.profile_form_class(request.POST, instance=request.user.shopuserprofile)

            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()

            else:
                user_form = self.user_form_class(instance=request.user)
                profile_form = self.profile_form_class(instance=request.user.shopuserprofile)

            return render(request, self.template_name, {'user_form': user_form, 'profile_form': profile_form, 'title': 'редактирование'})


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


def verify(request, email, key):
    user = ShopUser.objects.filter(email=email).first()
    if user:
        if user.activate_key == key and not user.is_activate_key_expired():
            user.activate_user()
            auth.login(request, user)
    return render(request, 'authapp/register-result.html')
