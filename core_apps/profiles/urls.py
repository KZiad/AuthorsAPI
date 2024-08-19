from django.urls import path
from .views import ProfileListAPIView, ProfileDetailAPIView, UpdateProfileAPIView, FollowAPIView, FollowerListView, FollowingListView, UnfollowAPIView

urlpatterns = [
    path("all/", ProfileListAPIView.as_view(), name="all-profiles"),
    path("me/", ProfileDetailAPIView.as_view(), name="my-profile"),
    path("me/update/", UpdateProfileAPIView.as_view(), name="update-profile"),
    path("me/following/", FollowingListView.as_view(), name="my-following"),
    path("me/followers/", FollowerListView.as_view(), name="my-followers"),
    path("<uuid:profile_id>/followers/", FollowerListView.as_view(), name="followers"),
    path("<uuid:profile_id>/follow/", FollowAPIView.as_view(), name="follow"),
    path("<uuid:profile_id>/unfollow/", UnfollowAPIView.as_view(), name="unfollow"),

]
