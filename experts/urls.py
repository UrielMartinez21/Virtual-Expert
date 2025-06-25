from django.urls import path
from . import views 

urlpatterns = [
    # To register a new user
    path('', views.my_virtual_experts, name='my_virtual_experts'),
    path('create_virtual_expert/', views.create_virtual_expert, name='create_virtual_expert'),

]