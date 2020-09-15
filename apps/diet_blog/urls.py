from django.urls import path

from .views import (PostCreateView, PostDeleteView, PostDetailView,
                    PostListView, PostUpdateView, UserPostListView, CommentCreateView, LikeView)

urlpatterns = [
    path("blog/", PostListView.as_view(), name="diet_composer-blog"),
    path("post/<int:pk>", PostDetailView.as_view(), name="post-detail"),
    path("post/new", PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
    path("user/<str:username>", UserPostListView.as_view(), name="user-posts"),
    path("post/<int:pk>/comment", CommentCreateView.as_view(), name="comment-create"),
    path('like/<int:pk>', LikeView, name="like_post"),
]
