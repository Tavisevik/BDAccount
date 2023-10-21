from accounts.views import *
from django.urls import path


urlpatterns = [
    path('', index, name='account'),    #http://127.0.0.1:8000/
    path('view/', RegistrationView.as_view(), name='view'),
    path('registration/', RegistrationUser.as_view(), name='registration'),
    #path('registration/', registration, name='registration'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('update/<int:user_id>/', RegistrationUser.as_view(), name='update_user'),
    path('delete/', RegistrationUser.as_view(), name='delete_user'),
    path('account-user/', account_user, name='account_user')
]