from django import template
from accounts.models import *

register = template.Library()

@register.simple_tag(name='getusers')
def get_users(filter=None, sort=None):
    if not filter:
        if not sort:
            return Account.objects.all()
        else:
            return Account.objects.order_by(sort)
    else:
        if not sort:
            return Account.objects.filter(pk=filter)
        else:
            return Account.objects.filter(pk=filter).sort_by(sort)

#@register.inclusion_tag('accounts/view.html')
#def show_accounts():
#    users = Account.objects.all()
#    return {'users': users}