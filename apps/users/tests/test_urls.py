from django.urls import resolve, reverse

from apps.users.views import profile, register


class TestUrls:
    def test_profile_url(self):
        url = reverse("profile")
        assert resolve(url).func == profile

    def test_register_url(self):
        url = reverse("register")
        assert resolve(url).func == register

    def test_login_url(self):
        path = reverse("login")
        assert resolve(path).view_name == "login"

    def test_logout_url(self):
        path = reverse("logout")
        assert resolve(path).view_name == "logout"

    def test_password_reset_url(self):
        path = reverse("password_reset")
        assert resolve(path).view_name == "password_reset"

    def test_password_reset_done_url(self):
        path = reverse("password_reset_done")
        assert resolve(path).view_name == "password_reset_done"

    def test_password_reset_confirm_url(self):
        path = reverse("password_reset_complete")
        assert resolve(path).view_name == "password_reset_complete"