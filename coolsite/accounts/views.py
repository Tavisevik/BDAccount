from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView
# from django.core.paginator import Paginator

from .forms import RegistrationForm
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
    # paginate_by = 4
    # paginate_orphans = 2
    template_name = 'accounts/view.html'
    context_object_name = 'data_users'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))

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


def registration(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            #print(form.cleaned_data)
            try:
                Account.objects.create(**form.cleaned_data)
                #form.save()
                return redirect('home')
            except:
                form.add_error(None, 'Ошибка добавления аккаунта')

    else:
        form = RegistrationForm()
    context = {
        'menu': menu,
        'title': 'Регистрация',
        'form': form,
    }
    return render(request, 'accounts/registration.html', context)

#def show_post(request):
#    context = {'menu': menu, 'title': 'Читать пост'}
#    return render(request, 'accounts/index.html', context=context)

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1> Страница не найдена </h1>')


def checking_user(login, password):
    pass


class RegistrationUser(View):
    def get(self, request):
        users = Account.objects.all()
        return render(request, 'registration.html',
                      {'users': users})


    def post(self, request):
        action = request.POST.get('action')

        if request.method == 'POST':
            if action == 'register':
                login = request.POST['login']
                email = request.POST['email']
                password = request.POST['password']

                if Account.objects.filter(email=email).exists():
                    messages.error(request, 'This email is already registered. Please log in.')
                    return redirect('login')

                registration = Account(fullname=login, email=email, password=password)
                registration.save()
                messages.success(request, 'Registration successful. Please log in.')
                return redirect('login')

            elif action == 'update':
                user_id = request.POST['user_id']
                user = get_object_or_404(Account, pk=user_id)
                user.login = request.POST['login']
                user.email = request.POST['email']
                user.password = request.POST['password']
                user.save()
                messages.success(request, 'Информация о пользователе успешно обновлена.')
                return redirect('registration')

            elif action == 'delete':
                user_id = request.POST['user_id']
                user = get_object_or_404(Account, pk=user_id)
                user.delete()
                messages.success(request, 'Пользователь успешно удален.')
                return redirect('registration')


class LoginUser(View):
    def get(self, request):
        return render(request, 'login.html')


    def post(self, request):
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']

            # Проверка, существует ли пользователь в локальной базе данных
            if Account.objects.filter(email=email, password=password).exists():
                # Пользователь аутентифицирован в локальной базе данных
                # Теперь проверка с внешним API
                if checking_user(email, password):
                    # Пользователь аутентифицирован с использованием API
                    # Выполнение действия входа, если необходимо
                    messages.success(request, 'Вход выполнен успешно.')
                    return redirect('dashboard')

            messages.error(request, 'Неверный email или пароль. Пожалуйста, попробуйте снова.')
            return redirect('login')
