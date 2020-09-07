import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from apps.diet_blog.models import Post


@pytest.mark.django_db
class TestView:
    @pytest.fixture(name="post", scope="class")
    def create_post(self):
        user = User(username="tm")
        post = Post.objects.create(
            title="Test post", content="Test content", author=user
        )

    def test_blog(self, client):
        response = client.get(reverse("diet_composer-blog"))
        assert response.status_code == 200
        assert "Main Page" in str(response.content)
        assert "Diet composer" in str(response.content)
        assert "diet_blog/blog.html" in [
            template.name for template in response.templates
        ]
