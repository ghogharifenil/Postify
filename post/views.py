from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import redirect
from .models import Post, Profile
from django.db.models import Q
from django.db.models import Count
from .decorators import login_require
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404



def about(request):
    return render(request, "post/about.html")


def help(request):
    return render(request, "post/help.html")


def setting(request):
    return render(request, "post/setting.html")


# @login_required
# def privacy(request):

#     profile = get_object_or_404(
#         Profile,
#         id=request.session["profile_id"]
#     )

#     if request.method == "POST":

#         profile.public_profile = bool(request.POST.get("public_profile"))
#         profile.show_city = bool(request.POST.get("show_city"))

#         profile.save()

#         return redirect("privacy")

#     return render(request, "post/privacy.html", {
#         "profile_user": profile
#     })


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
def home(request):
    posts = Post.objects.filter(
        user__public_profile=True
    ).order_by("-created_at")

    top_users = Profile.objects.annotate(
        total_posts=Count('posts')
    ).order_by('-total_posts')[:10]

    context = {

        "posts": posts,
        "top_users": top_users,

    }

    return render(
        request,
        "post/home.html",
        context
    )


# @login_required
# def user_profile(request,id):

#     user = get_object_or_404(
#         Profile,
#         id=id
#     )

#     posts = Post.objects.filter(
#         user=user
#     ).order_by("-created_at")

#     return render(
#         request,
#         "post/user_profile.html",
#         {
#             "profile_user":user,
#             "posts":posts
#         }
#     )
@login_require
def user_profile(request, id):

    user = get_object_or_404(Profile, id=id)

    current_user = get_object_or_404(
        Profile,
        id=request.session["profile_id"]
    )

    # PRIVATE CHECK
    if not user.public_profile and user.id != current_user.id:
        return render(request, "post/private.html", {
            "profile_user": user
        })

    posts = Post.objects.filter(user=user)

    return render(request, "post/user_profile.html", {
        "profile_user": user,
        "posts": posts,
        "current_user": current_user
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

    # login check
    if not request.session.get("profile_id"):
        return redirect("login")

    current_user = Profile.objects.get(
        id=request.session["profile_id"]
    )

    if request.method == "POST":

        title = request.POST.get("title")
        content = request.POST.get("content")
        image = request.FILES.get("image")

        Post.objects.create(

            user=current_user,
            title=title,
            content=content,
            image=image

        )

        return redirect("/")

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

    return render(
        request,
        'post/profile.html',
        {
            'current_user': current_user,
            'posts': posts
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
