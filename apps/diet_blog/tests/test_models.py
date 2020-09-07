import pytest
from django.contrib.auth.models import User

from apps.diet_blog.models import Post


@pytest.mark.django_db()
class TestModels:
    @pytest.fixture(scope="class", name="post")
    def create_models(self):
        user = User(username="tm")
        post = Post(title="Test Post", content="test content", author=user)
        return post

    def test_blog_obj_name(self, post):
        assert repr(post) == "Post title: Test Post"

    def test_post(self, post):
        assert isinstance(post, Post)
        assert post.title == "Test Post"
        assert post.content == "test content"
        assert post.author.username == "tm"
