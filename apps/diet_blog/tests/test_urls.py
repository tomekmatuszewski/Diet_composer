from django.urls import resolve, reverse


class TestUrls:
    def test_detail_url(self):
        path = reverse("diet_composer-blog")
        assert resolve(path).view_name == "diet_composer-blog"
