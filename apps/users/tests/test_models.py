from django.contrib.auth.models import User
import pytest


@pytest.mark.django_db(True)
class TestModels:

    def test_user_profile(self):
        user = User.objects.create_user(
            username="testuser",
            email="demo@demo.com",
            password="test12345"
        )
        assert user.profile
        assert user.profile.image.url == '/media/default.jpg'

