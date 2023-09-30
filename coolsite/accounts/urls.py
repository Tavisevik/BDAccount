from accounts.views import *
from django.urls import path


urlpatterns = [
    path('', index, name='account'),    #http://127.0.0.1:8000/
    path('view/', viewData, name='view'),
    path('registration/', RegistrationUser.as_view(), name='registration'),
    path('login/', RegistrationUser.as_view(), name='login'),
    path('update/<int:user_id>/', RegistrationUser.as_view(), name='update_user'),
    path('delete/<int:user_id>/', RegistrationUser.as_view(), name='delete_user'),
    #path('post'<int:post_id>/', show_post, name='post')
]