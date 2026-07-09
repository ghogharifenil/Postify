from .models import Notification
from account.models import Profile

def notification_count(request):

    if "profile_id" not in request.session:
        return {}

    profile = Profile.objects.get(id=request.session["profile_id"])

    count = Notification.objects.filter(
        receiver=profile,
        is_read=False
    ).count()

    return {
        "unread_notifications": count
    }