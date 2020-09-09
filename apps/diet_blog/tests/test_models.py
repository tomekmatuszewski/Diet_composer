import pytest
from django.contrib.auth.models import User

from apps.diet_blog.models import Post


@pytest.mark.django_db()
class TestModels:
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
        assert repr(post) == "Post title: Test post"

    def test_post(self, post):
        assert isinstance(post, Post)
        assert post.title == "Test post"
        assert post.content == "Test content"
        assert post.author.username == "test_user"
