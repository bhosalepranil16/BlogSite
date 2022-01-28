from django.contrib import admin

from .models import PostModel, CommentModel, LikeModel


# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'author')
    list_filter = ('date', 'author')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'owner')
    list_filter = ('post', 'owner')


class LikeAdmin(admin.ModelAdmin):
    list_display = ('post', 'owner', 'is_liked')
    list_filter = ('post', 'owner')


admin.site.register(PostModel, PostAdmin)
admin.site.register(CommentModel, CommentAdmin)
admin.site.register(LikeModel, LikeAdmin)
