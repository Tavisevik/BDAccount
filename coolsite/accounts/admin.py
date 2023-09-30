from django.contrib import admin

from .models import *


class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'login', 'email', 'password', 'created_time', 'updated_time')
    list_display_link = ('id', 'login')
    search_fields = ('login', 'email')
    list_editable = ('login',)
    list_filter = ('created_time', 'login', )
    prepopulated_fields = {'slug': ('login',)}


admin.site.register(Account, AccountAdmin)