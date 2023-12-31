from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils import timezone
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import User, Post


def index(request):
    posts = Post.objects.all().order_by('-date')

    items_per_page = 10

    paginator = Paginator(posts, items_per_page)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'posts': posts,
    }
    return render(request, "network/index.html", context)


@require_POST
def add_post(request):
    data = json.loads(request.body)
    content = data.get('content', '')
    owner = request.user

    if content and owner:
        new_post = Post.objects.create(
            owner=owner,
            date=timezone.now(),
            content=content
        )
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid data'})
    
    
@csrf_exempt
def edit_post(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        post_id = data.get('post_id')
        content = data.get('content')

        post = Post.objects.get(pk=post_id)
        post.content = content
        post.save()

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})


@require_POST
def like_post(request):
    data = json.loads(request.body)
    post_id = data.get('post_id', '')
    user = request.user

    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Post does not exist'})

    if user in post.likes.all():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        liked = True

    post.save()

    return JsonResponse({'status': 'success', 'liked': liked, 'like_count': post.likes.count()})


@login_required
def following(request):
    current_user = request.user
    following_users = current_user.following.all()
    posts = Post.objects.filter(owner__in=following_users).order_by('-date')

    posts_per_page = 10
    paginator = Paginator(posts, posts_per_page)
    
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'posts': posts,
    }

    return render(request, "network/following.html", context)


@login_required
def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(owner=profile_user).order_by('-date')

    items_per_page = 10

    paginator = Paginator(posts, items_per_page)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    followers_count = profile_user.followers.count()
    following_count = profile_user.following.count()

    is_following = False
    if request.user.is_authenticated and request.user != profile_user:
        is_following = request.user.following.filter(pk=profile_user.pk).exists()

    return render(request, 'network/profile.html', {
        'profile_user': profile_user,
        'posts': posts,
        'followers_count': followers_count,
        'following_count': following_count,
        'is_following': is_following,
    })
    

@login_required
def toggle_follow(request, username):
    profile_user = get_object_or_404(User, username=username)

    if request.user.is_authenticated and request.user != profile_user:
        if request.user.following.filter(pk=profile_user.pk).exists():
            request.user.following.remove(profile_user)
        else:
            request.user.following.add(profile_user)

    return HttpResponseRedirect(reverse('profile', args=[username]))


def login_view(request):
    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        print(f'user: {user}, {username}, {password}')

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })
            
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username or email already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
