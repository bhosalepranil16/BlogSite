from django.contrib.auth.models import User
from django import forms

from .models import PostModel, CommentModel


class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']
        labels = {
            'username': 'Username :',
            'password': 'Password :',
            'first_name': 'First Name :',
            'last_name': 'Last Name :',
            'email': 'Email :'
        }


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=128)

    class Meta:
        labels = {
            'username': 'Username :',
            'password': 'Password :'
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = PostModel
        fields = '__all__'
        exclude = ['date', 'author']


class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        exclude = ['owner', 'post']
        labels = {
            'text': 'Comment :'
        }
