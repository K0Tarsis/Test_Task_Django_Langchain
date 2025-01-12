from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from chat_bot.filters import HomesFilter
from chat_bot.models import Homes, ChatMessage, Chat
from chat_bot.paginators import ThreeItemPagination
from chat_bot.serializers import HomesSerializer, ScraperTaskSerializer, ChatMessageSerializer, ChatSerializer, \
    ChatUpdateSerializer, AddMessageToChatSerializer
from chat_bot.task import scrape_homes


class HomesViewSet(ReadOnlyModelViewSet):
    serializer_class = HomesSerializer
    queryset = Homes.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = HomesFilter
    http_method_names = ['get', 'delete', 'post']
    pagination_class = ThreeItemPagination


class ChatViewSet(ModelViewSet):
    queryset = Chat.objects.all()
    http_method_names = ['get', 'patch', 'delete', 'post']

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return ChatUpdateSerializer

        return ChatSerializer

    @swagger_auto_schema(
        request_body=ChatUpdateSerializer,
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class ChatMessageViewSet(ModelViewSet):
    queryset = ChatMessage.objects.all()
    http_method_names = ['get', 'patch', 'delete', 'post']
    serializer_class = ChatMessageSerializer


class TriggerScraping(APIView):

    @swagger_auto_schema(
        request_body=ScraperTaskSerializer,
    )
    def post(self, request, *args, **kwargs):
        serializer_class = ScraperTaskSerializer(data=request.data)
        serializer_class.is_valid(raise_exception=True)
        task = scrape_homes.delay(serializer_class.validated_data['all_pages'])
        return Response(
            {"task_id": task.id}
        )

class AddMessageToChat(APIView):

    @swagger_auto_schema(
        request_body=AddMessageToChatSerializer,
    )
    def post(self, request, *args, **kwargs):
        serializer = AddMessageToChatSerializer(data=request.data)
        if serializer.is_valid():
            chat = serializer.save()
            data = serializer.validated_data
            data['chat_id'] = chat.id
            return Response(data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)