from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import redirect
from .models import Post , Profile
from django.db.models import Q
from django.db.models import Count

def home(request):


   

    posts = Post.objects.all().order_by('-created_at')

    top_users = Profile.objects.annotate(
        total_posts=Count('posts')
    ).order_by('-total_posts')[:10]

    context={

        "posts":posts,
        "top_users":top_users,
       
    }

    return render(
        request,
        "post/home.html",
        context
    )



def user_profile(request,id):

    user = get_object_or_404(
        Profile,
        id=id
    )

    posts = Post.objects.filter(
        user=user
    ).order_by("-created_at")

    return render(
        request,
        "post/user_profile.html",
        {
            "profile_user":user,
            "posts":posts
        }
    )


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

def create_post(request):

    # login check
    if not request.session.get("profile_id"):
        return redirect("login")


    current_user=Profile.objects.get(
        id=request.session["profile_id"]
    )


    if request.method=="POST":

        title=request.POST.get("title")
        content=request.POST.get("content")
        image=request.FILES.get("image")

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
            "current_user":current_user
        }
    )
def profile(request):

    current_user=Profile.objects.get(
        id=request.session['profile_id']
    )

    posts=Post.objects.filter(
        user=current_user
    ).order_by('-id')

    return render(
        request,
        'post/profile.html',
        {
            'current_user':current_user,
            'posts':posts
        }
    )