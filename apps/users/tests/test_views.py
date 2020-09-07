import pytest
from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory
from django.urls import reverse
from mixer.backend.django import mixer

from apps.users.views import profile, register


@pytest.mark.django_db
class TestView:
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
