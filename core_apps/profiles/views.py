from django.shortcuts import render

# TODO: change in production
from Authors_API.settings.local import DEFAULT_FROM_EMAIL
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from .exceptions import CantFollowYourself
from .models import Profile
from .pagination import ProfilePagination
from .renderers import ProfileJSONRenderer, ProfilesJSONRenderer
from .serializers import ProfileSerializer, FollowingSerializer, UpdateProfileSerializer


User = get_user_model()


class ProfileListAPIView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    pagination_class = ProfilePagination

    renderer_classes = [ProfilesJSONRenderer]


class ProfileDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    renderer_classes = [ProfilesJSONRenderer]

    def get_queryset(self):
        queryset = Profile.objects.select_related("user")
        return queryset

    def get_object(self):
        user = self.request.user
        profile = self.get_queryset().get(user=user)
        return profile


class UpdateProfileAPIView(generics.RetrieveAPIView):
    serializer_class = UpdateProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]
    renderer_classes = [ProfileJSONRenderer]

    def get_object(self):
        profile = self.request.user.profile
        return profile

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class FollowingListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            profile = Profile.objects.get(user__id=request.user.id)
            following_profiles = profile.following.all()
            serializer = FollowingSerializer(following_profiles, many=True)
            formatted_response = {
                "status_code": status.HTTP_200_OK,
                "following_count": following_profiles.count(),
                "users_i_follow": serializer.data
            }
            return Response(formatted_response, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class FollowerListView(APIView):
    def get(self, request, profile_id=None, format=None):
        try:
            if profile_id is None:
                profile = Profile.objects.get(user__id=request.user.id)
            else:
                profile = Profile.objects.get(id=profile_id)
            follower_profiles = profile.followers.all()
            serializer = FollowingSerializer(follower_profiles, many=True)
            formatted_response = {
                "status_code": status.HTTP_200_OK,
                "followers_count": follower_profiles.count(),
                "followers": serializer.data
            }
            return Response(formatted_response, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class FollowAPIView(APIView):
    def post(self, request, profile_id, format=None):
        try:
            follower = Profile.objects.get(user=self.request.user)
            user_profile = request.user.profile

            # BUG: DJango can't find users by id for some reason
            profile = Profile.objects.get(id=profile_id)

            if follower == profile:
                raise CantFollowYourself
            if user_profile.check_following(profile):
                formatted_response = {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": f"you are already following {profile.user.first_name} {profile.user.last_name}"
                }
                return Response(formatted_response, status=status.HTTP_400_BAD_REQUEST)

            user_profile.follow(profile)
            subject = "A new user follows you"
            message = f"Hello {profile.user.first_name}!, {user_profile.user.first_name} {user_profile.user.last_name} is now following you."
            from_email = DEFAULT_FROM_EMAIL
            to_emails = [profile.user.email]
            send_mail(subject=subject, message=message, from_email=from_email,
                      recipient_list=to_emails, fail_silently=True)
            return Response({
                "status_code": status.HTTP_200_OK,
                "message": f"You are now following {profile.user.first_name} {profile.user.last_name}"
            })
        except Profile.DoesNotExist:
            raise NotFound("You can't follow a profile that does not exist.")


class UnfollowAPIView(APIView):
    def post(self, request, profile_id, *args, **kwargs):
        user_profile = request.user.profile
        profile = Profile.objects.get(id=profile_id)
        try:
            follower = Profile.objects.get(user=self.request.user)
            if not user_profile.check_following(profile):
                formatted_response = {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": f"You are not following {profile.user.first_name} {profile.user.last_name}"
                }
                return Response(formatted_response, status=status.HTTP_400_BAD_REQUEST)

            user_profile.unfollow(profile)
            return Response({
                "status_code": status.HTTP_200_OK,
                "message": f"You have successfully unfollowed {profile.user.first_name} {profile.user.last_name}"
            }, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
