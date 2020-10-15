import pytest
from django.contrib.auth.models import User

from apps.users.models import Profile


@pytest.mark.django_db(True)
class TestModels:
    @pytest.fixture(name="user", scope="class")
    def create_post(self, django_db_blocker, django_db_setup):
        with django_db_blocker.unblock():
            user = User.objects.create_user(
                username="test_user", email="test@demo.pl", password="test12345"
            )
        yield user
        with django_db_blocker.unblock():
            user.delete()

    def test_user_profile(self, user):
        assert user.profile
        assert str(user.profile) == "test_user profile"
        assert user.profile.image.url == "/media/default.jpg"
