from account.models import Profile
from django.shortcuts import get_object_or_404, redirect, render
from .models import Post, Profile, Notification, Like, PostImage
from django.db.models import Q,  Count
from .decorators import login_require
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta


@login_require
def home(request):

    current_user = Profile.objects.get(
        id=request.session["profile_id"]
    )

    posts = Post.objects.filter(
        user__public_profile=True
    ).order_by("-created_at")

    top_users = Profile.objects.annotate(
        total_posts=Count("posts")
    ).order_by("-total_posts")[:10]

    liked_posts = Like.objects.filter(
        user=current_user
    ).values_list("post_id", flat=True)

    context = {
        "posts": posts,
        "top_users": top_users,
        "current_user": current_user,
        "liked_posts": liked_posts,
    }

    return render(
        request,
        "post/home.html",
        context
    )


@login_require
def about(request):
    return render(request, "post/about.html")


@login_require
def help(request):
    return render(request, "post/help.html")


@login_require
def setting(request):
    return render(request, "post/setting.html")


@login_require
def privacy(request):

    profile = get_object_or_404(
        Profile,
        id=request.session["profile_id"]
    )

    if request.method == "POST":

        profile.public_profile = request.POST.get("public_profile") == "on"
        profile.show_city = request.POST.get("show_city") == "on"

        profile.save()

        return redirect("privacy")

    return render(request, "post/privacy.html", {
        "profile": profile
    })


@login_require
def edit_profile(request):

    profile = Profile.objects.get(
        id=request.session['profile_id']
    )

    if request.method == "POST":

        profile.name = request.POST.get('name')

        profile.bio = request.POST.get('bio')
        profile.city = request.POST.get('city')
        if request.FILES.get('profile_pic'):
            profile.profile_pic = (
                request.FILES['profile_pic']
            )

        profile.save()

        return redirect('profile')

    return render(
        request,
        'post/edit_profile.html',
        {'profile': profile}
    )


@login_require
def user_profile(request, id):

    user = get_object_or_404(Profile, id=id)

    current_user = get_object_or_404(
        Profile,
        id=request.session["profile_id"]
    )

    liked_posts = Like.objects.filter(
        user=current_user
    ).values_list("post_id", flat=True)

    # PRIVATE CHECK
    if not user.public_profile and user.id != current_user.id:
        return render(request, "post/private.html", {
            "profile_user": user
        })

    posts = Post.objects.filter(user=user)

    return render(request, "post/user_profile.html", {
        "profile_user": user,
        "posts": posts,
        "current_user": current_user,
        'liked_posts': liked_posts
    })


@login_require
def search_page(request):

    query = request.GET.get("q")

    posts = Post.objects.none()
    profile = None

    if query:

        # user profile search
        profile = Profile.objects.filter(
            Q(username__icontains=query) |
            Q(name__icontains=query)
        ).first()

        # posts search
        posts = Post.objects.filter(

            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__name__icontains=query) |
            Q(user__username__icontains=query)

        )

    return render(
        request,
        "post/search.html",
        {
            "posts": posts,
            "query": query,
            "profile": profile
        }
    )

@login_require
def create_post(request):

    current_user = Profile.objects.get(
        id=request.session["profile_id"]
    )

    if request.method == "POST":

        title = request.POST.get("title")
        content = request.POST.get("content")

        # Multiple Images
        images = request.FILES.getlist("images")

        # Backward compatibility (single image)
        single_image = request.FILES.get("image")

        post = Post.objects.create(

            user=current_user,
            title=title,
            content=content,
            image=single_image

        )

        # Save Multiple Images
        for image in images:
            PostImage.objects.create(
                post=post,
                image=image
            )

        # Notification
        users = Profile.objects.exclude(id=current_user.id)

        for user in users:

            Notification.objects.create(

                sender=current_user,
                receiver=user,
                post=post,
                notification_type="new_post"

            )

        return redirect("home")

    return render(
        request,
        "post/create_post.html",
        {
            "current_user": current_user
        }
    )


@login_require
def profile(request):

    current_user = Profile.objects.get(
        id=request.session['profile_id']
    )

    posts = Post.objects.filter(
        user=current_user
    ).order_by('-id')

    liked_posts = Like.objects.filter(
        user=current_user
    ).values_list("post_id", flat=True)

    return render(
        request,
        'post/profile.html',
        {
            'current_user': current_user,
            'posts': posts,
            'liked_posts': liked_posts,
        }
    )


@login_require
def save_post(request, id):

    profile = Profile.objects.get(
        id=request.session['profile_id']
    )

    post = Post.objects.get(id=id)

    saved = False

    if profile in post.saved_by.all():

        post.saved_by.remove(profile)

        saved = False

    else:

        post.saved_by.add(profile)

        saved = True

    return JsonResponse({
        'saved': saved
    })


@login_require
def saved_posts(request):

    profile = Profile.objects.get(
        id=request.session['profile_id']
    )

    posts = profile.saved_posts.all()

    return render(
        request,
        'post/saved.html',
        {
            'posts': posts,
            'current_user': profile
        }
    )


@login_require
def delete_account(request):

    profile = get_object_or_404(
        Profile,
        id=request.session["profile_id"]
    )

    if request.method == "POST":

        # delete profile
        profile.delete()

        # clear session
        request.session.flush()

        return redirect("login")

    return render(request, "post/delete_account.html", {
        "profile": profile
    })


@login_require
def notifications(request):

    if "profile_id" not in request.session:
        return redirect("login")

    # 24 કલાકથી જૂની notifications delete
    Notification.objects.filter(
        created_at__lt=timezone.now() - timedelta(hours=24)
    ).delete()

    profile = Profile.objects.get(
        id=request.session["profile_id"]
    )

    notifications = Notification.objects.filter(
        receiver=profile
    )

    notifications.update(is_read=True)

    return render(
        request,
        "post/notifications.html",
        {
            "notifications": notifications,
            "current_user": profile,
        },
    )


@login_require
def notification_count_api(request):

    current_user = Profile.objects.get(
        id=request.session["profile_id"]
    )

    count = Notification.objects.filter(
        receiver=current_user,
        is_read=False
    ).count()

    return JsonResponse({
        "count": count
    })


@login_require
def edit_post(request, post_id):

    current_user = Profile.objects.get(
        id=request.session["profile_id"]
    )

    post = get_object_or_404(
        Post,
        id=post_id,
        user=current_user
    )

    if request.method == "POST":

        post.title = request.POST.get("title")
        post.content = request.POST.get("content")

        if request.FILES.get("image"):
            post.image = request.FILES.get("image")

        post.save()

        return redirect("home")   # અથવા home

    return render(
        request,
        "post/edit_post.html",
        {
            "post": post,
            "current_user": current_user
        }
    )


@login_require
def delete_post(request, post_id):

    current_user = Profile.objects.get(
        id=request.session["profile_id"]
    )

    post = get_object_or_404(
        Post,
        id=post_id,
        user=current_user
    )

    if request.method == "POST":
        post.delete()
        return redirect("home")   # અથવા home

    return render(
        request,
        "post/delete_post.html",
        {
            "post": post,
            "current_user": current_user
        }
    )


@login_require
def toggle_like(request, post_id):
    profile = Profile.objects.get(
        id=request.session["profile_id"]
    )
    post = get_object_or_404(Post, id=post_id)

    like = Like.objects.filter(user=profile, post=post)

    if like.exists():
        like.delete()
        liked = False
    else:
        Like.objects.create(user=profile, post=post)
        liked = True

    return JsonResponse({
        "liked": liked,
        "total_likes": post.total_likes(),
    })

from django.http import JsonResponse
from .models import Post

@login_require
def like_users(request, post_id):

    post = get_object_or_404(Post, id=post_id)

    likes = []

    for like in post.likes.select_related("user"):

        profile = like.user

        likes.append({
            "id": profile.id,
            "name": profile.name,
            "profile_pic": profile.profile_pic.url if profile.profile_pic else ""
        })

    return JsonResponse({
        "likes": likes
    })