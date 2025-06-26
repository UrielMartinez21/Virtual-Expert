from django.urls import path
from . import views 

urlpatterns = [
    path('', views.my_virtual_experts, name='my_virtual_experts'),

    # to create virtual expert
    path('create_virtual_expert/', views.create_virtual_expert, name='create_virtual_expert'),
    path('send_data_to_expert/', views.send_data_to_expert, name='send_data_to_expert'),

    # to train model
    path('train/<slug:slug>/', views.train_virtual_expert, name='train_virtual_expert'),
    path('send_data_to_train/', views.send_data_to_train, name='send_data_to_train'),

    path('delete/<slug:slug_expert>/', views.delete_expert, name='delete_expert'),
]