from django.contrib import admin

from .models import *


class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'fullname', 'email', 'password', 'created_time', 'updated_time')
    list_display_link = ('id', 'fullname')
    search_fields = ('email',)
    list_editable = ('email',)
    list_filter = ('created_time', 'email', )
    #prepopulated_fields = {'slug': ('login',)}


admin.site.register(Account, AccountAdmin)
