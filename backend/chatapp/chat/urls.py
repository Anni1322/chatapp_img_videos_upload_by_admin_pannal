from django.urls import path
from .views import *

urlpatterns = [
    path('chat/', chat_view, name='chat_view'),
    path('add_qestion/', ChatModelCreateView.as_view(), name='ChatModelCreateView'),
    path('list/', ChatModelListCreateView.as_view(), name='chat-list-create'),
]
