from django.urls import path , include
from . import views
urlpatterns = [
    path('',views.landing,name="landing"),
    path('login/',views.login,name="login"),
    path('registration/',views.register_step1,name="register"),
    path('register_step2/',views.register_step2,name="register_step2"),
    path('logout/',views.logout,name="logout"),
    
]