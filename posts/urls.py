from django.urls import path, include
from .views import *

urlpatterns = [
    path("follow/", follow_index, name="follow_index"),
    path('', MyView.as_view(), name='index'),
    path('new/', NewView.as_view(), name='new'),
    path('<str:username>/', ProfileView.as_view(), name='profile'),
    path('<str:username>/<int:post_id>/edit/', post_edit, name='post_edit'),
    path('<int:post_id>/delete/', post_delete, name='post_delete'),
    path('<int:pk>', PostView.as_view(), name='post_view'),
    path("<str:username>/follow/", profile_follow,
         name="profile_follow"),
    path("<str:username>/unfollow/", profile_unfollow,
         name="profile_unfollow"),
]
