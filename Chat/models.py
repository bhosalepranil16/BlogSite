from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class MessageModel(models.Model):
    message = models.TextField()
    room_name = models.CharField(max_length=100)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver_messages')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

