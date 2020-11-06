import pytest
from django.contrib.auth.models import User

from apps.users.models import UserActivity


@pytest.mark.django_db(True)
class TestModels:
    @pytest.fixture(name="user", scope="class")
    def create_user_obj(self, django_db_blocker, django_db_setup):
        with django_db_blocker.unblock():
            user = User.objects.create_user(
                username="test_user", email="test@demo.pl", password="test12345",
            )
        yield user
        with django_db_blocker.unblock():
            user.delete()

    def test_user_profile(self, user):
        assert user.profile
        assert str(user.profile) == "test_user profile"
        assert user.profile.image.url == "/media/default.jpg"

    def test_profile_properties(self, user):
        activity = UserActivity.objects.create(factor=1.2, description="activity")
        user.profile.age = 25
        user.profile.height = 190
        user.profile.gender = "Male"
        user.profile.weight = 80
        user.profile.activity = activity
        assert user.profile.cmr == 2242
        assert user.profile.bmr == 1868.7
        assert user.profile.daily_proteins == 112.0
        assert user.profile.daily_carb == 308.0
        assert user.profile.daily_fats == 62
