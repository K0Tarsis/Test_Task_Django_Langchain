from django.db.models import ForeignKey
from rest_framework import serializers
from .models import Homes, ChatMessage, Chat


class HomesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homes
        fields = '__all__'


class ScraperTaskSerializer(serializers.Serializer):
    all_pages = serializers.BooleanField(default=False, help_text="Parse all pages?")

    class Meta:
        fields = ['all_pages']


class ChatMessageSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(read_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = ChatMessage
        fields = ['id', 'timestamp', 'sender', 'message']


class ChatSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many=True, read_only=True)

    class Meta:
        model = Chat
        fields = ['id', 'messages']


class ChatUpdateSerializer(serializers.ModelSerializer):
    messages = serializers.PrimaryKeyRelatedField(many=True, queryset=ChatMessage.objects.all())

    class Meta:
        model = Chat
        fields = ['id', 'messages']


class AddMessageToChatSerializer(serializers.ModelSerializer):
    message = ChatMessageSerializer(many=False, required=False)
    chat_id = serializers.IntegerField(required=False)

    class Meta:
        model = Chat
        fields = ['message', 'chat_id']

    def create(self, validated_data):
        message_data = validated_data['message']
        chat_id = validated_data.get('chat_id', None)

        if chat_id:
            try:
                chat_instance = Chat.objects.get(pk=chat_id)
            except Chat.DoesNotExist:
                raise serializers.ValidationError(f"Chat with id {chat_id} does not exist.")
        else:
            chat_instance = Chat.objects.create()

        if message_data:
            ChatMessage.objects.create(chat=chat_instance, **message_data)

        else:
            raise serializers.ValidationError("Message data is required.")

        chat_instance.refresh_from_db()
        return chat_instance