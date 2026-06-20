from .models import Profile

def user_context(request):

    profile_id = request.session.get("profile_id")

    user = None

    if profile_id:
        user = Profile.objects.filter(id=profile_id).first()

    return {
        "current_user": user
    }