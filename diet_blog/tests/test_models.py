import pytest
from django.contrib.auth.models import User

from diet_blog.models import Post


@pytest.mark.django_db(True)
def test_post():
    user = User(username="tm")
    post = Post(title="Test Post", content="test content", author=user)
    assert isinstance(post, Post)
    assert post.title == "Test Post"
    assert post.content == "test content"
    assert user.username == "tm"
