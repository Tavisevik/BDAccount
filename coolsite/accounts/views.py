from django.contrib.auth import logout, login, get_user_model, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView
# from django.core.paginator import Paginator

from .forms import RegistrationForm, LoginForm
from .models import Account
from .utils import *
from django.contrib import messages
import requests

def index(request): #HttpRequest
    context = {
        'menu': menu,
        'title': 'Главная страница'
    }
    return render(request, 'accounts/index.html', context=context)

class RegistrationView(DataMixin, ListView):

    model = Account
    template_name = 'accounts/view.html'
    context_object_name = 'users'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Просмотр')
        #c_def_ = self.get_user_context(users=Account.objects.all())
        return dict(list(context.items()) + list(c_def.items()) )

    def get_queryset(self):
        #return Account.objects.filter(login__contains='sya')
        return Account.objects.filter()

# def viewData(request):
#     users = Account.objects.all()
#     #users = get_object_or_404(Account)
#     context = {
#         'menu': menu,
#         'title': 'Аккаунты'
#     }
#     return render(request, 'accounts/view.html', context=context)


# def registration(request):
#
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             #print(form.cleaned_data)
#             try:
#                 Account.objects.create(**form.cleaned_data)
#                 #form.save()
#                 return redirect('home')
#             except:
#                 form.add_error(None, 'Ошибка добавления аккаунта')
#
#     else:
#         form = RegistrationForm()
#     context = {
#         'menu': menu,
#         'title': 'Регистрация',
#         'form': form,
#     }
#     return render(request, 'accounts/registration.html', context)

#def show_post(request):
#    context = {'menu': menu, 'title': 'Читать пост'}
#    return render(request, 'accounts/index.html', context=context)

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1> Страница не найдена </h1>')


def checking_user(email, password):
    pass


class RegistrationUser(DataMixin, CreateView):
    form_class = RegistrationForm
    template_name = 'accounts/registration.html'
    success_url = reverse_lazy('registration')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))

    # def form_valid(self, form):
    #     user = form.save()
    #     login(self.request, user)
    #     return redirect('/view')

    # def post(self, request):
    #     if request.method == 'POST':
    #         email = request.POST['email']
    #         password = request.POST['password']
    #         if Account.objects.filter(email=email).exists():
    #             messages.error(request, 'Пользователь существует. Пожалуйста, вместо регистрации, войдите в аккаунт.')
    #             return redirect('login')

    # def get(self, request):
    #     users = Account.objects.all()
    #     return render(request, 'registration.html',
    #                   {'users': users})

    #
    # def post(self, request):
    #     action = request.POST.get('action')
    #
    #     if request.method == 'POST':
    #         if action == 'register':
    #             fullname = request.POST['fullname']
    #             email = request.POST['email']
    #             password = request.POST['password']
    #
    #             if Account.objects.filter(email=email).exists():
    #                 messages.error(request, 'This email is already registered. Please log in.')
    #                 return redirect('login')
    #
    #             registration = Account(fullname=fullname, email=email, password=password)
    #             registration.save()
    #             messages.success(request, 'Registration successful. Please log in.')
    #             return redirect('login')
    #
    #         elif action == 'update':
    #             user_id = request.POST['user_id']
    #             user = get_object_or_404(Account, pk=user_id)
    #             user.login = request.POST['login']
    #             user.email = request.POST['email']
    #             user.password = request.POST['password']
    #             user.save()
    #             messages.success(request, 'Информация о пользователе успешно обновлена.')
    #             return redirect('registration')
    #
    #         elif action == 'delete':
    #             user_id = request.POST['user_id']
    #             user = get_object_or_404(Account, pk=user_id)
    #             user.delete()
    #             messages.success(request, 'Пользователь успешно удален.')
    #             return redirect('registration')


class LoginUser(DataMixin, CreateView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('view')


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Войти')

        return dict(list(context.items()) + list(c_def.items()))

    # def form_valid(self, form):
    #     user = form.save()
    #
    #     login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
    #     return redirect('/view')

    def post(self, request):
        action = request.POST.get('action')
        if request.method == 'POST':


            email = request.POST['email']
            password = request.POST['password']

            # Проверка, существует ли пользователь в локальной базе данных
            if Account.objects.filter(email=email, password=password).exists():
                #Account.objects.filter(email=email,)
                from django.contrib.auth import get_user
                #user = get_user(self.request)
                user = Account.objects.get(email=email)

                #email = request.POST["email"]
                #password = request.POST["password"]
                #user = authenticate(request, username=email, password=password)
                # if user is not None:
                #     login(request, user)
                #     # Redirect to a success page.
                #     return redirect('view')
                # else:
                #     # Return an 'invalid login' error message.
                #     print('*************** Return an invalid login error message.')
                #user.is_active = True
                #print('------------------', user, user.id)
                #user.save()

                #login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
                # Пользователь аутентифицирован в локальной базе данных
                # Теперь проверка с внешним API
                # if checking_user(email, password):
                    # Пользователь аутентифицирован с использованием API
                    # Выполнение действия входа, если необходимо
                messages.success(request, 'Вход выполнен успешно.')
                return redirect('view')

    #     if request.method == 'POST':
    #         email = request.POST['email']
    #         password = request.POST['password']
    #
    #         # Проверка, существует ли пользователь в локальной базе данных
    #         if Account.objects.filter(email=email, password=password).exists():
    #             # Пользователь аутентифицирован в локальной базе данных
    #             # Теперь проверка с внешним API
    #             if checking_user(email, password):
    #                 # Пользователь аутентифицирован с использованием API
    #                 # Выполнение действия входа, если необходимо
    #                 messages.success(request, 'Вход выполнен успешно.')
    #                 return redirect('dashboard')
    #
    #         messages.error(request, 'Неверный email или пароль. Пожалуйста, попробуйте снова.')
    #         return redirect('accountuser')


def logout_user(request):
    logout(request)
    return redirect('login')


def account_user(request):
    if request.method == 'POST':
        print(request)
    return redirect('view')
