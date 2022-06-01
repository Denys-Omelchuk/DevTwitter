from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Post, Comment


def home(request):
    q = request.GET.get('q')
    profiles = None
    users_posts = None
    if request.GET.get('q') is not None:
        profiles = User.objects.filter(
            username__icontains=q
        )[:3]
        users_posts = Post.objects.filter(
            body__icontains=q
        )
    posts = Post.objects.all()
    if request.method == 'POST':
        posts = Post.objects.create(
            host=request.user,
            body=request.POST.get('body')
        )
        return redirect('home')
    context = {
        'posts': posts,
        'profiles': profiles,
        'users_posts': users_posts
    }

    return render(request, 'base/home.html', context)


def loginPage(request):

    if request.user.is_authenticated:
        return redirect('home')

    page = 'login'
    if request == 'post':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request, 'home')

    return render(request, 'base/login_register.html', {'page': page})


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
    return render(request, 'base/login_register.html', {'form': form})


def post_info(request, pk):
    post = Post.objects.get(id=pk)
    comments = post.comment_set.all().order_by('-created')

    if request.method == 'POST':
        comments = Comment.objects.create(
            host=request.user,
            post=post,
            body=request.POST.get('body')
        )
        return redirect('post', pk=post.id)

    content = {
        'post': post,
        'comments': comments,
    }
    return render(request, 'base/post.html', content)
















