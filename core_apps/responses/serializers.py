from rest_framework import serializers
from .models import Response


class ResponseSerializer(serializers.ModelSerializer):
    user_first_name = serializers.CharField(source="user.first_name", read_only=True)
    article_title = serializers.CharField(source="article.title", read_only=True)
    responses_count = serializers.SerializerMethodField()

    def get_responses_count(self, obj):
        replies = Response.objects.filter(parent_response=obj)
        return replies.count()

    class Meta:
        model = Response
        fields = [
            "pkid",
            "id",
            "user_first_name",
            "article_title",
            "parent_response",
            "responses_count",
            "body",
            "created_at"
        ]


class ResponseDetailSerializer(ResponseSerializer):
    responses = serializers.SerializerMethodField()

    def get_responses(self, obj):
        replies = Response.objects.filter(parent_response=obj)
        return ResponseSerializer(replies, many=True).data

    class Meta:
        model = Response
        fields = [
            "pkid",
            "id",
            "user_first_name",
            "article_title",
            "parent_response",
            "responses_count",
            "responses",
            "body",
            "created_at"
        ]
