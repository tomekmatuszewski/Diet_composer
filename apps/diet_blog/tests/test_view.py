import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from apps.diet_blog.models import Post


@pytest.mark.django_db
class TestView:

    @pytest.fixture(name="post", scope="class")
    def create_post(self, django_db_blocker, django_db_setup):
        with django_db_blocker.unblock():
            user = User.objects.create_user(username="test_user", email="test@demo.pl", password="test12345")
            post = Post.objects.create(
                title="Test post", content="Test content", author=user
            )
        yield post
        with django_db_blocker.unblock():
            post.delete()
            user.delete()

    def test_blog(self, client, post):
        response = client.get(reverse("diet_composer-blog"))
        assert response.status_code == 200
        assert "Main Page" in str(response.content)
        assert "Diet composer" in str(response.content)
        assert "diet_blog/blog.html" in [
            template.name for template in response.templates
        ]
        assert post.content == "Test content"
        assert post.author.username == "test_user"
        assert post.author.email == "test@demo.pl"
