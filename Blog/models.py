from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class PostModel(models.Model):
    title = models.CharField(max_length=50)
    excerpt = models.CharField(max_length=300)
    content = models.TextField()
    image = models.ImageField(upload_to='posts')
    slug = models.SlugField(max_length=50, unique=True, db_index=True)
    date = models.DateField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='posts')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'


class CommentModel(models.Model):
    text = models.CharField(max_length=500)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='comments')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'


class LikeModel(models.Model):
    is_liked = models.BooleanField(default=False)
    date = models.DateField(auto_now=True)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='likes')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'
