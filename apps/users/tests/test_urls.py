from django.urls import reverse, resolve


class TestUrls:

    def test_register_url(self):
        path = reverse("register")
        assert resolve(path).view_name == "register"

    def test_login_url(self):
        path = reverse("login")
        assert resolve(path).view_name == "login"

    def test_logout_url(self):
        path = reverse("logout")
        assert resolve(path).view_name == "logout"

    def test_profile_url(self):
        path = reverse("profile")
        assert resolve(path).view_name == "profile"