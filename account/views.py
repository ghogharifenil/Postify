from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from .models import Profile
from .forms import RegisterStep1Form, RegisterStep2Form

def landing(request):
    return render(request,"profile/landing.html")


def register_step1(request):

    if request.method == "POST":

        form = RegisterStep1Form(request.POST)

        if form.is_valid():

            user = Profile.objects.create(

                name=form.cleaned_data["name"],
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                city=form.cleaned_data["city"],

                password=make_password(
                    form.cleaned_data["password"]
                )
            )

            request.session["customer_id"] = user.id

            return redirect("register_step2")

    else:
        form = RegisterStep1Form()

    return render(request, "profile/register_step1.html", {"form": form})

def register_step2(request):

    customer_id = request.session.get("customer_id")

    if not customer_id:
        return redirect("register_step1")

    user = Profile.objects.get(id=customer_id)

    if request.method == "POST":

        form = RegisterStep2Form(request.POST, request.FILES)

        if form.is_valid():

            user.bio = form.cleaned_data["bio"]
            user.profile_pic = form.cleaned_data["profile_pic"]
            user.save()

            return redirect("login")

    else:
        form = RegisterStep2Form()

    return render(request, "profile/register_step2.html", {"form": form})

from django.contrib.auth.hashers import check_password

def login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = Profile.objects.get(username=username)

            if check_password(password, user.password):

                request.session["profile_id"] = user.id
                request.session['profile_pic'] = user.profile_pic.url
                request.session["profile_name"] = user.name

                return redirect("home")

            else:
                return render(request, "profile/login.html", {
                    "error": "Invalid password"
                })

        except Profile.DoesNotExist:

            return render(request, "profile/login.html", {
                "error": "User not found"
            })

    return render(request, "profile/login.html")

def logout(request):
    request.session.flush()
    return redirect("landing")