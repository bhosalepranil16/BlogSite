from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import IndexView, SignUpView, CreatePostView, PostDetailView, AllPostsView, like_post_view, ProfileView

urlpatterns = [
    path('', IndexView.as_view(), name='index_page'),

    path('sign-up', SignUpView.as_view(), name='signup_page'),
    path('login', LoginView.as_view(template_name='Blog/login.html'), name='login_page'),
    path('logout', LogoutView.as_view(), name='logout'),

    path('all-posts', AllPostsView.as_view(), name='all-posts'),
    path('create-post', CreatePostView.as_view(), name='create_post'),
    path('post/<slug:slug>', PostDetailView.as_view(), name='post_detail'),
    path('like/<slug:slug>', like_post_view, name='like'),

    path('profile/<str:username>', ProfileView.as_view(), name='profile_page')
]
