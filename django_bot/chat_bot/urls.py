from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import HomesViewSet, TriggerScraping, ChatMessageViewSet, ChatViewSet, AddMessageToChat

router = DefaultRouter()
router.register(r'chat_messages', ChatMessageViewSet, basename='chat_message')
router.register(r'chats', ChatViewSet, basename='chat')
router.register(r'homes', HomesViewSet, basename='home')


urlpatterns = [
    path('scrapping/', TriggerScraping.as_view(), name='trigger_task_api'),
    path('add_message/', AddMessageToChat.as_view(), name='add_message')
]

urlpatterns += router.urls
