from django.urls import path
from . import views 

urlpatterns = [
    # To register a new user
    path('register/', views.register_user, name='register_user'),
    path('create/', views.create_user, name='create_user'),

    # To login a user
    path('login/', views.login_user, name='login_user'),
    path('send_data_to_login/', views.send_data_to_login, name='send_data_to_login'),

    # To logout a user
    path('logout_user/', views.logout_user, name='logout_user'),
]