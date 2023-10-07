from django import forms
from django.core.exceptions import ValidationError
import re
from .models import *

class RegistrationForm(forms.Form):
    login = forms.CharField(max_length=255, label="Логин", widget=forms.TextInput(attrs={'class': 'form-input'}))
    slug = forms.SlugField(max_length=255, label="URL")
    email = forms.CharField(max_length=255, label="Email", widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password = forms.CharField(max_length=255, label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Account
        fields = ('login', 'slug', 'email', 'password', )
        # widgets = {
        #     'login': forms.TextInput(attrs={'class': 'form-input'}),
        #     'slug': forms.TextInput(attrs={'class': 'form-input'}),
        #     'email': forms.TextInput(attrs={'class': 'form-input'}),
        #     'password': forms.TextInput(attrs={'class': 'form-input'}),
        # }

    def clean_login(self):
        regex = re.compile(r'([A-Za-z]+[0-9]+[.-_])*[A-Za-z0-9]+')
        login = self.cleaned_data['login']
        if not (len(login) <= 100 and re.fullmatch(regex, login)):
            raise ValidationError('Длина превышает 100 символов  или содержит недопустимые символы')

        return login

    def clean_email(self):
        regex = re.compile(r'([A-Za-z]+[0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        email = self.cleaned_data['email']
        if not re.fullmatch(regex, email):
            raise ValidationError('Некорректный email')

        return email

    def clean_password(self):
        regex = re.compile(r'[A-Za-z0-9-_#$]{10,}')
        password = self.cleaned_data['password']
        if not re.fullmatch(regex, password):
            raise ValidationError('Некорректный пароль (A-Za-z0-9-_#$ длина от 10)')

        return password