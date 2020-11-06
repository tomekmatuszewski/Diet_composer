import os
from pathlib import Path

import pytest
from django.contrib.auth.models import AnonymousUser, User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory
from django.urls import reverse
from mixer.backend.django import mixer

from apps.users.views import profile

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent.parent


@pytest.mark.django_db
class TestView:
    @pytest.fixture(name="user", scope="class")
    def create_post(self, django_db_blocker, django_db_setup):
        with django_db_blocker.unblock():
            user = User.objects.create_user(
                username="test_user", email="test@demo.pl", password="test12345"
            )
        yield user
        with django_db_blocker.unblock():
            os.remove(user.profile.image.path)
            user.delete()

    def test_profile_view_authenticated(self):
        path = reverse("profile")
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)

        response = profile(request)
        assert response.status_code == 200

    def test_profile_view_unauthenticated(self):
        path = reverse("profile")
        request = RequestFactory().get(path)
        request.user = AnonymousUser()

        response = profile(request)
        assert response.status_code == 302
        assert "login" in response.url

    def test_register(self, client):
        response = client.get(reverse("register"))
        assert response.status_code == 200
        assert "Username" in str(response.content)
        assert "Password" in str(response.content)
        assert "Email" in str(response.content)
        assert "users/register.html" in [
            template.name for template in response.templates
        ]

    def test_register_user_post(self, client):
        response = client.post(
            reverse("register"),
            {
                "username": "test_user",
                "email": "test@gmail.com",
                "password1": "test12345",
                "password2": "test12345",
            },
        )
        assert response.status_code == 302
        assert User.objects.first().username == "test_user"
        assert User.objects.first().email == "test@gmail.com"

    def test_register_user_post_fail(self, client):
        response = client.post(
            reverse("register"),
            {
                "username": "test_user",
                "email": "test@gmail.com",
                "password1": "test12",
                "password2": "test12",
            },
        )
        assert response.status_code == 200
        assert not User.objects.first()
        assert User.objects.count() == 0
        assert (
            "This password is too short. It must contain at least 8 characters."
            in str(response.content)
        )

    def test_post_update(self, client, user):
        image_path = os.path.join(BASE_DIR, "media/test_pics/joker.jpg")
        client.login(username="test_user", password="test12345")
        response = client.post(
            reverse("profile"),
            {
                "username": "test_user1",
                "email": "test1@gmail.com",
                "image": SimpleUploadedFile(
                    name="joker.jpg",
                    content=open(image_path, "rb").read(),
                    content_type="image/jpg",
                ),
            },
        )
        user.refresh_from_db()
        assert response.status_code == 302
        assert user.username == "test_user1"
        assert user.email == "test1@gmail.com"
        assert user.profile.image.path == os.path.join(
            BASE_DIR, "media/profile_pics/joker.jpg"
        )
