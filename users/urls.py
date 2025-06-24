from django.urls import path
from . import views 

urlpatterns = [
    # To register a new user
    path('register_user/', views.register_user, name='register_user'),
    path('create_user/', views.create_user, name='create_user'),

    # To login a user
    path('login_user/', views.login_user, name='login_user'),
    path('send_data_to_login/', views.send_data_to_login, name='send_data_to_login'),

    # To logout a user
    path('logout_user/', views.logout_user, name='logout_user'),

    # To see the dashboard of the user
    path('dashboard/', views.dashboard, name='dashboard'),
    path('virtual_experts/', views.virtual_experts, name='virtual_experts'),
    path('create_virtual_expert/', views.create_virtual_expert, name='create_virtual_expert'),

]