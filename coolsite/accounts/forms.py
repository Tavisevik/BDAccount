from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
import re
from .models import *

class RegistrationForm(forms.ModelForm):
    fullname = forms.CharField(max_length=255, label="Полное имя", widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.CharField(max_length=255, label="Email", widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password = forms.CharField(max_length=255, label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    USERNAME_FIELD = 'email'

    class Meta:
        model = Account
        fields = ('fullname', 'email', 'password', )


    def clean_login(self):
        regex = re.compile(r'([A-Za-z]+)*[A-Za-z0-9]+')
        fullname = self.cleaned_data['fullname']
        if not (len(fullname) <= 100 and re.fullmatch(regex, fullname)):
            raise ValidationError('Длина превышает 100 символов  или содержит недопустимые символы')

        return fullname

    def clean_email(self):
        regex = re.compile(r'([A-Za-z]+[0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        email = self.cleaned_data['email']
        if not re.fullmatch(regex, email):
            raise ValidationError('Некорректный email')

        return email

    def clean_password(self):
        regex = re.compile(r'[A-Za-z0-9-_#$]{5,}')
        password = self.cleaned_data['password']
        if not re.fullmatch(regex, password):
            raise ValidationError('Некорректный пароль (A-Za-z0-9-_#$ длина от 5)')

        return password


class LoginForm(forms.ModelForm):
    email = forms.CharField(max_length=255, label="Email", widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password = forms.CharField(max_length=255, label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    USERNAME_FIELD = 'email'
    last_login = 'email'


    class Meta:
        model = Account
        fields = ('email', 'password', )

    def clean_email(self):
        email = self.cleaned_data['email']

        if not Account.objects.filter(email=email).exists():
            raise ValidationError('Еmail не зарегистрирован')
        return email

    def clean_password(self):
        password = self.cleaned_data['password']

        if not Account.objects.filter(password=password).exists():
            raise ValidationError('Некорректный пароль')

        return password