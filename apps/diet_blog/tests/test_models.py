import pytest
from django.contrib.auth.models import User

from apps.diet_blog.models import Comment, Post


@pytest.mark.django_db()
class TestPost:
    @pytest.fixture(name="post", scope="class")
    def create_post(self, django_db_blocker, django_db_setup):
        with django_db_blocker.unblock():
            user = User.objects.create_user(
                username="test_user", email="test@demo.pl", password="test12345"
            )
            post = Post.objects.create(
                title="Test post", content="Test content", author=user
            )
        yield post
        with django_db_blocker.unblock():
            post.delete()
            user.delete()

    def test_blog_obj_name(self, post):
        assert str(post) == "Post 1, title: Test post"

    def test_post(self, post):
        assert isinstance(post, Post)
        assert post.title == "Test post"
        assert post.content == "Test content"
        assert post.author.username == "test_user"
        assert post.total_likes() == 0


@pytest.mark.django_db()
class TestComment:
    @pytest.fixture(name="comment", scope="class")
    def create_post(self, django_db_blocker, django_db_setup):
        with django_db_blocker.unblock():
            user = User.objects.create_user(
                username="test_user", email="test@demo.pl", password="test12345"
            )
            post = Post.objects.create(
                title="Test post", content="Test content", author=user
            )
            comment = Comment.objects.create(
                content="Test content", author=user, post=post
            )
        yield comment
        with django_db_blocker.unblock():
            comment.delete()
            post.delete()
            user.delete()

    def test_blog_obj_name(self, comment):
        assert str(comment) == "Comment 1 to post Test post"

    def test_post(self, comment):
        assert isinstance(comment, Comment)
        assert comment.content == "Test content"
        assert comment.author.username == "test_user"
