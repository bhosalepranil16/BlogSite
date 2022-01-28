from django.shortcuts import render, reverse, get_object_or_404
from django.views import View
from django.views.generic import ListView
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

from .forms import SignUpForm, PostForm, CommentForm
from .models import PostModel, LikeModel


# Create your views here.

class IndexView(View):
    def get(self, request):
        try:
            return render(request, 'Blog/index.html')
        except:
            return render(request, 'Blog/index.html')


class AllPostsView(ListView):
    template_name = 'Blog/all-posts.html'
    model = PostModel
    context_object_name = 'posts'

    def get_queryset(self):
        query_set = super().get_queryset()
        data = query_set.order_by('-id')
        return data


class SignUpView(View):
    def get(self, request):
        signup_form = SignUpForm()
        return render(request, 'Blog/sign-up.html', {
            'signup_form': signup_form
        })

    def post(self, request):
        signup_form = SignUpForm(data=request.POST)
        if signup_form.is_valid():
            user = signup_form.save(commit=False)
            user.set_password(request.POST['password'])
            user.save()
            return HttpResponseRedirect(reverse('login_page'))
        return render(request, 'Blog/sign-up.html', {
            'signup_form': signup_form
        })


class CreatePostView(View):
    def get(self, request):
        post_form = PostForm()
        return render(request, 'Blog/create-post.html', {
            'post_form': post_form
        })

    def post(self, request):
        post_form = PostForm(request.POST, request.FILES)
        if request.user.is_anonymous:
            return render(request, 'Blog/create-post.html', {
                'post_form': post_form
            })
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.save()
            return HttpResponseRedirect(reverse('post_detail', args=[post.slug]))
        return render(request, 'Blog/create-post.html', {
            'post_form': post_form
        })


class PostDetailView(View):

    def is_liked(self, post, owner):
        likes_no = LikeModel.objects.filter(post_id=post.id, is_liked=True).count()
        if owner.is_anonymous:
            return False, likes_no
        liked, _ = LikeModel.objects.get_or_create(post_id=post.id, owner_id=owner.id)
        return liked.is_liked, likes_no

    def get(self, request, slug):
        post = get_object_or_404(PostModel, slug=slug)
        comment_form = CommentForm()
        liked, likes_no = self.is_liked(post, request.user)
        return render(request, 'Blog/post-detail.html', {
            'post': post,
            'comments': post.comments.all().order_by('-id'),
            'comment_form': comment_form,
            'liked': liked,
            'likes_no': likes_no
        })

    def post(self, request, slug):
        user = request.user
        if user.is_anonymous:
            return HttpResponseRedirect(reverse('post_detail', args=[slug]))
        comment_form = CommentForm(request.POST)
        post = get_object_or_404(PostModel, slug=slug)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.owner = user
            comment.save()
        liked, likes_no = self.is_liked(post, request.user)
        return render(request, 'Blog/post-detail.html', {
            'post': post,
            'comment_form': comment_form,
            'comments': post.comments.all().order_by('-id'),
            'liked': liked,
            'likes_no': likes_no
        })


def like_post_view(request, slug):
    post = get_object_or_404(PostModel, slug=slug)
    owner = request.user
    if owner.is_anonymous:
        return HttpResponseRedirect(reverse('post_detail', args=[slug]))
    like, _ = LikeModel.objects.get_or_create(post_id=post.id, owner_id=owner.id)
    like.is_liked = not like.is_liked
    like.save()
    return HttpResponseRedirect(reverse('post_detail', args=[slug]))


class ProfileView(View):
    def get(self, request, username):
        posts = PostModel.objects.filter(author__username=username)
        profile = User.objects.get(username=username)
        return render(request, 'Blog/profile.html', {
            'posts': posts,
            'profile': profile
        })
