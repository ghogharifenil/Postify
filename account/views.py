from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import Profile
from .forms import RegisterStep1Form, RegisterStep2Form
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404

# Landing Page
def landing(request):

    # Jo user login hoy to direct home par moklo
    if request.session.get("profile_id"):
        return redirect("home")

    return render(request, "profile/landing.html")


# Register Step 1
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

    return render(
        request,
        "profile/register_step1.html",
        {"form": form}
    )


# Register Step 2
def register_step2(request):

    customer_id = request.session.get("customer_id")

    if not customer_id:
        return redirect("register_step1")

    try:
        user = Profile.objects.get(id=customer_id)

    except Profile.DoesNotExist:
        return redirect("register_step1")

    if request.method == "POST":

        form = RegisterStep2Form(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            user.bio = form.cleaned_data["bio"]
            user.profile_pic = form.cleaned_data["profile_pic"]

            user.save()

            # Registration session remove
            del request.session["customer_id"]

            return redirect("login")

    else:
        form = RegisterStep2Form()

    return render(
        request,
        "profile/register_step2.html",
        {"form": form}
    )


# Login
def login(request):

    # Jo pehla thi login hoy to login page na dekhado
    if request.session.get("profile_id"):
        return redirect("home")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = Profile.objects.get(
                username=username
            )

            if check_password(
                password,
                user.password
            ):

                request.session["profile_id"] = user.id
                request.session["profile_name"] = user.name

                if user.profile_pic:
                    request.session["profile_pic"] = user.profile_pic.url

                # 30 divas sudhi login rahe
                request.session.set_expiry(
                    60 * 60 * 24 * 30
                )

                return redirect("home")

            else:

                return render(
                    request,
                    "profile/login.html",
                    {
                        "error": "Invalid password"
                    }
                )

        except Profile.DoesNotExist:

            return render(
                request,
                "profile/login.html",
                {
                    "error": "User not found"
                }
            )

    return render(
        request,
        "profile/login.html"
    )


# Logout
def logout(request):

    request.session.flush()

    return redirect("landing")



def home(request):

    if not request.session.get("profile_id"):
        return redirect("login")

    return render(
        request,
        "profile/home.html"
    )


