
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following", views.following, name="following"),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('toggle_follow/<str:username>/', views.toggle_follow, name='toggle_follow'),
    
    #API Routes
    path('add_post/', views.add_post, name='add_post'),
    path('like_post/', views.like_post, name='like_post'),
    path('edit_post/', views.edit_post, name='edit_post'),
]
