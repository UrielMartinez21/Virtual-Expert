from django.urls import path
from . import views 

urlpatterns = [
    path('', views.manage_virtual_experts, name='manage_virtual_experts'),

    # to create virtual expert
    path('create/', views.create_expert, name='create_expert'),
    path('delete/<slug:slug_expert>/', views.delete_expert, name='delete_expert'),

    # to train model
    path('train/<slug:slug>/', views.train_virtual_expert, name='train_virtual_expert'),
    path('send_data_to_train/', views.send_data_to_train, name='send_data_to_train'),

    # chat
    path('chat/<slug:slug>/', views.chat_virtual_expert, name='chat_virtual_expert'),
]