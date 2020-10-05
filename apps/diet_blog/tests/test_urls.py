import pytest
from django.contrib.auth.models import User
from django.urls import resolve, reverse

from apps.diet_blog.models import Comment, Post
from apps.diet_blog.views import (CommentCreateView, CommentDeleteView,
                                  CommentUpdateView, LikeView, PostCreateView,
                                  PostDeleteView, PostDetailView, PostListView,
                                  PostUpdateView, UserPostListView)


@pytest.mark.django_db()
class TestUrls:
    @pytest.fixture(scope="class", name="user")
    def create_user_obj(self, django_db_blocker):
        with django_db_blocker.unblock():
            user = User.objects.create_user(username="testuser", password="test12345")
            yield user
        with django_db_blocker.unblock():
            user.delete()

    @pytest.fixture(scope="class", name="post")
    def create_post_obj(self, django_db_blocker, user):
        with django_db_blocker.unblock():
            post = Post.objects.create(
                title="Test post", content="Test content", author=user
            )
            yield post
        with django_db_blocker.unblock():
            post.delete()

    def test_blog_url(self):
        url = reverse("diet_composer-blog")
        assert resolve(url).func.view_class == PostListView

    def test_post_url(self, post):
        url = reverse("post-detail", kwargs={"pk": post.id})
        assert resolve(url).func.view_class == PostDetailView

    def test_create_post_url(self):
        url = reverse("post-create")
        assert resolve(url).func.view_class == PostCreateView

    def test_update_post_url(self, post):
        url = reverse("post-update", kwargs={"pk": post.id})
        assert resolve(url).func.view_class == PostUpdateView

    def test_delete_post_url(self, post):
        url = reverse("post-delete", kwargs={"pk": post.id})
        assert resolve(url).func.view_class == PostDeleteView

    def test_user_posts_url(self, user):
        url = reverse("user-posts", kwargs={"username": user.username})
        assert resolve(url).func.view_class == UserPostListView

    def test_user_comment_url(self, user, post):
        comment = Comment.objects.create(content="Test content", author=user, post=post)
        url = reverse("comment-create", kwargs={"pk": comment.pk})
        assert resolve(url).func.view_class == CommentCreateView

    def test_user_comment_update_url(self, user, post):
        comment = Comment.objects.create(content="Test content", author=user, post=post)
        url = reverse("comment-update", kwargs={"pk": comment.pk})
        assert resolve(url).func.view_class == CommentUpdateView

    def test_user_comment_delete_url(self, user, post):
        comment = Comment.objects.create(content="Test content", author=user, post=post)
        url = reverse("comment-delete", kwargs={"pk": comment.pk})
        assert resolve(url).func.view_class == CommentDeleteView

    def test_like_url(self, user):
        url = reverse("like-post", kwargs={"pk": user.pk})
        assert resolve(url).func == LikeView
