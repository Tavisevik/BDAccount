from django.shortcuts import render

from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Account
from django.contrib import messages
import requests

menu = ["Аккаунты"]


def index(request): #HttpRequest
        return render(request, 'accounts/index.html', {'menu': menu, 'title': 'Главная страница'})

def viewData(request):
    users = Account.objects.all()
    return render(request, 'accounts/view.html', {'users': users, 'menu': menu, 'title': 'Аккаунты'})


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
