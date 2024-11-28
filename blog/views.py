from django.shortcuts import render

def index(request):
    return render(request, 'blog/index.html')

from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'public']

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})
class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriber')
    subscribed_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscribed_to')


@login_required
def subscribe(request, user_id):
    user_to_subscribe = User.objects.get(id=user_id)
    Subscription.objects.create(user=request.user, subscribed_to=user_to_subscribe)
    return redirect('index')

@login_required
def unsubscribe(request, user_id):
    Subscription.objects.filter(user=request.user, subscribed_to_id=user_id).delete()
    return redirect('index')


@login_required
def subscribed_posts(request):
    subscriptions = Subscription.objects.filter(user=request.user)
    posts = Post.objects.filter(author__in=[s.subscribed_to for s in subscriptions])
    return render(request, 'blog/subscribed_posts.html', {'posts': posts})





