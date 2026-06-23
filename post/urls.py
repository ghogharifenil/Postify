from django.urls import path, include
from . import views
urlpatterns = [

    path('home/', views.home, name="home"),
    path(
        "user-profile/<int:id>/",
        views.user_profile,
        name="user_profile"
    ),
    path(
    "search/",
    views.search_page,
    name="search"
),
path(
"create/",
views.create_post,
name="create_post"
),

path('profile/',views.profile,name="profile")
]
