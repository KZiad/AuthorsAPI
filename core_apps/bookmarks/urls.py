from django.urls import path
from .views import BookmarkCreateView, BookmarkDestroyView

urlpatterns = [
    path("bookmark_article/<uuid:article_id>/", BookmarkCreateView.as_view(), name="create-bookmark"),
    path("remove_bookmark/<uuid:article_id>/", BookmarkDestroyView.as_view(), name="remove-bookmark")
]
