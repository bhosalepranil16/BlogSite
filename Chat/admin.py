from django.contrib import admin

from .models import MessageModel


# Register your models here.

class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver')
    list_filter = ('room_name', 'sender', 'receiver')


admin.site.register(MessageModel, MessageAdmin)
