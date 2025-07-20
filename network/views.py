import json

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse

from django.core.paginator import Paginator

from .models import User, Post


def index(request):
    posts = Post.objects.all().order_by("-timestamp")
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html",{
        "posts": posts,
        "page_obj": page_obj
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
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


@login_required
def post(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == "GET":
        return JsonResponse(post.serialize())
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data["likecount"] == True:
            post.likecount += 1
            post.save()
        elif data["likecount"] == False: 
            post.likecount -= 1
            post.save()
        return JsonResponse(post.serialize(), status=200)
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)



def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required
def compose(request):
    
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    data = json.loads(request.body)
    postcontent = data.get("postcontent", "")
    if postcontent == '':
        return JsonResponse({"error": "Cannot make an empty post."}, status=400)
    post = Post.objects.create(user = request.user,
                postcontent = postcontent)
    post.save()
    return JsonResponse({"message": "Post sent successfully."}, status=201)

@login_required
def allposts(request):
    posts = Post.objects.all()
    posts = posts.order_by("-timestamp").all()
    return JsonResponse([post.serialize() for post in posts], safe=False)

@login_required
def userposts(request, user):
   
    try:
        user_obj = User.objects.get(username=user)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=400)
    
    posts = Post.objects.filter(user=user_obj).order_by("-timestamp").all()
    
    return render(request, "network/user.html", {
        "posts": posts,
        "user": user_obj,
        "followingcount": user_obj.following.count(),
        "followercount": user_obj.followers.count()
    })

@login_required
def followingposts(request, user):
    followingposts = []
    try:
        user_obj = User.objects.get(username=user)
        following = user_obj.following.all()
        for follow in following:
            follow_obj =  User.objects.get(username=follow)
            followingposts += Post.objects.filter(user=follow_obj).order_by("-timestamp").all()
            
        paginator = Paginator(followingposts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=400)
    
    return render(request, "network/following.html", {
        "posts": followingposts,
        'page_obj': page_obj
        
    })


@login_required
def edit(request, postId):
    post_obj = Post.objects.get(pk = postId)
    if request.method == "GET":
        if post_obj.user == request.user.username:
            return JsonResponse({"error": "This is not your post"}, status=400)
        else:
            return render(request, "network/post.html", {
            "post": post_obj,
            "user": post_obj.user,
        })
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data["postcontent"]:
            post_obj.postcontent = data["postcontent"]
            post_obj.save()
            return JsonResponse(post_obj.serialize(), status=200)



@login_required
def follow(request, user):
    if user == request.user.username:
        return JsonResponse({"error": "Cannot follow yourself"}, status=400)
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)
    try:
            followed_obj = User.objects.get(username=user)
            follower_obj = User.objects.get(username=request.user.username)
    except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=400)
    data = json.loads(request.body)
    if data["following"] == True:
            follower_obj.following.add(followed_obj)
    if data["following"] == False:
            follower_obj.following.remove(followed_obj)
    
    return JsonResponse({
        "followingcount": follower_obj.following.count(),
        "followerscount": followed_obj.followers.count()
    }, status=200)