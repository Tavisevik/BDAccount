from .models import *

menu = [{'title': 'Главная', 'url_name': 'account'},
        {'title': 'Аккаунты', 'url_name': 'view'},
        #{'title': 'Изменить', 'url_name': 'update_user'},
        {'title': 'Удалить', 'url_name': 'delete_user'},
        ]


class DataMixin:
    paginate_by = 4

    def get_user_context(self, **kwargs):
        context = kwargs
        # cats = Category.objects.annotate(Count('women'))

        user_menu = menu.copy()
        # if not self.request.user.is_authenticated:
        #     user_menu.pop(1)

        context['menu'] = user_menu

        # context['cats'] = cats
        # if 'cat_selected' not in context:
        #     context['cat_selected'] = 0
        return context