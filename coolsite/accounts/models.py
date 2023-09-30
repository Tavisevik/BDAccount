from django.db import models
from django.urls import reverse


class Account(models.Model):
    login = models.CharField(max_length=100, verbose_name='Логин')
    email = models.EmailField(verbose_name='Почта')
    password = models.CharField(max_length=30, verbose_name='Пароль')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='Дата последнего доступа')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')


    def __str__(self):
        return self.login


    def get_absolute_url(self):
        return reverse('user_id', kwargs={'user_id': self.pk})

    class Meta:
        verbose_name = 'Аккаунты пользователей'
        verbose_name_plural = 'Аккаунты пользователей'
        ordering = ['created_time', 'login']

