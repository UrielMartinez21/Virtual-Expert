from django.urls import path
from . import views 

urlpatterns = [
    path('', views.my_virtual_experts, name='my_virtual_experts'),
    path('create_virtual_expert/', views.create_virtual_expert, name='create_virtual_expert'),
    path('send_data_to_expert/', views.send_data_to_expert, name='send_data_to_expert'),
]