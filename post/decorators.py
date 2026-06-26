from functools import wraps
from django.shortcuts import redirect

def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        customer_id = request.session.get("profile_id")

        if not customer_id:
            return redirect("login")

        return view_func(request, *args, **kwargs)

    return wrapper