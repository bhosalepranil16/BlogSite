from django.contrib import admin

from .models import MessageModel


# Register your models here.

class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver')
    list_filter = ('room_name', 'sender', 'receiver')
    ordering = ('-created_at',)

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(MessageModel, MessageAdmin)
