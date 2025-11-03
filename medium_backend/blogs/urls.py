from django.urls import path
from .views import PostView, CommentView, LikeView, PostSearchView

urlpatterns = [
    path("", PostView.as_view()),
    path("posts/", PostView.as_view()),
    path("posts/<int:post_id>/", PostView.as_view()),
    path("comments/", CommentView.as_view()),
    path("comments/<int:comment_id>/", CommentView.as_view()),
    path("like/", LikeView.as_view()),
    path('search/', PostSearchView.as_view()),
    
]
