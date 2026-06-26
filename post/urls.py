from django.urls import path, include
from . import views
urlpatterns = [

    path('about/',views.about,name="about"),
    path('help/',views.help,name="help"),
    path('home/', views.home, name="home"),
    path('user-profile/<int:id>/', views.user_profile,name="user_profile"),
    path('search/',views.search_page, name="search"),
    path('create/',views.create_post,name="create_post"),

    path('profile/', views.profile, name="profile"),
    path('save_post/<int:id>/', views.save_post, name="save_post"),
    path('saved_posts/',views.saved_posts,name="saved_posts"),

]
