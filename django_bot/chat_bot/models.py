from django.db import models

from chat_bot.constant import RENT_ALIAS, SALE_ALIAS, SALE_VALUE, RENT_VALUE


class Homes(models.Model):

    TYPE_OF_PURCHASE = {
        RENT_ALIAS: RENT_VALUE,
        SALE_ALIAS: SALE_VALUE,
    }

    title = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    bedrooms = models.IntegerField(null=True, blank=True)
    bathrooms = models.IntegerField(null=True, blank=True)
    area = models.IntegerField(null=True, blank=True)
    type_of_purchase = models.CharField(choices=TYPE_OF_PURCHASE)
    summary = models.TextField(null=False, blank=False)


    def __str__(self):
        return self.title


class Chat(models.Model):

    def __str__(self):
        return f"Chat {self.pk}"


class ChatMessage(models.Model):
    SENDER_CHOICES = [
        ('user', 'User'),
        ('bot', 'Bot'),
    ]

    timestamp = models.DateTimeField(auto_now_add=True)
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES)
    message = models.TextField()
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)

    def __str__(self):
        return f"[{self.timestamp}] {self.sender}: {self.message[:50]}"