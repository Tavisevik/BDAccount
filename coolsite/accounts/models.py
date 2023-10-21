from django.db import models
from django.urls import reverse


class Account(models.Model):
    fullname = models.CharField(max_length=100, verbose_name='Полное имя')
    email = models.EmailField(verbose_name='Почта')
    password = models.CharField(max_length=30, verbose_name='Пароль')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='Дата последнего доступа')
    USERNAME_FIELD = 'email'
    last_login = 'email'

    def __str__(self):
        return self.email


    def get_absolute_url(self):
        return reverse('user_id', kwargs={'user_id': self.pk})

    class Meta:
        verbose_name = 'Аккаунты пользователей'
        verbose_name_plural = 'Аккаунты пользователей'
        ordering = ['created_time', 'email']

