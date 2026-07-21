from django.urls import path, include
from . import views


urlpatterns = [


    path('home/', views.home, name="home"),
    path('search/',views.search_page, name="search"),


    path('about/',views.about,name="about"),
    path('help/',views.help,name="help"),


    path('setting/',views.setting,name="setting"),
    path('edit_profile/',views.edit_profile,name="edit_profile"),
    path('privacy/',views.privacy,name="privacy"),
    path("delete_account/", views.delete_account, name="delete_account"),


    path('user-profile/<int:id>/', views.user_profile,name="user_profile"),
    path('profile/', views.profile, name="profile"),

    path('create/',views.create_post,name="create_post"),
    path('save_post/<int:id>/', views.save_post, name="save_post"),
    path('saved_posts/',views.saved_posts,name="saved_posts"),
    path('edit_post/<int:post_id>/',views.edit_post,name="edit_post"),
    path('delete_post/<int:post_id>/',views.delete_post,name="delete_post"),

    
    
    path('notifications/',views.notifications,name="notifications"),
    path("notification-count/",views.notification_count_api,name="notification_count_api",),

    path('like/<int:post_id>/', views.toggle_like, name="toggle_like"),
    path("like_users/<int:post_id>/",views.like_users,name="like_users"),
]
