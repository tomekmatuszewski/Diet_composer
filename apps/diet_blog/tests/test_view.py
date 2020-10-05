import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from apps.diet_blog.models import Comment, Post


@pytest.mark.django_db
class TestPostView:
    @pytest.fixture(name="post", scope="class")
    def create_post(self, django_db_blocker, django_db_setup):
        with django_db_blocker.unblock():
            user = User.objects.create_user(
                username="test_user", email="test@demo.pl", password="test12345"
            )
            post = Post.objects.create(
                title="Test post", content="Test content", author=user
            )
        yield post
        with django_db_blocker.unblock():
            post.delete()
            user.delete()

    def test_blog_view(self, client, post):
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

    def test_post_detail_view(self, client, post):
        response = client.get(reverse("post-detail", kwargs={"pk": post.pk}))
        assert response.status_code == 200
        assert post.content == "Test content"
        assert post.author.username == "test_user"
        assert "diet_blog/post_detail.html" in [
            template.name for template in response.templates
        ]
        assert post.author.profile.image.url == "/media/default.jpg"

    def test_post_update_view(self, client, post):
        client.login(username="test_user", password="test12345")
        response = client.post(
            reverse("post-update", kwargs={"pk": post.pk}),
            {
                "title": "test_post111",
                "content": "newcontent",
            },
        )
        post.refresh_from_db()
        assert response.status_code == 302
        assert post.content == "newcontent"
        assert post.title == "test_post111"

    def test_post_create_view(self, client):
        client.login(username="test_user", password="test12345")
        response = client.post(
            reverse("post-create"),
            {
                "title": "new_post",
                "content": "new post content",
            },
        )
        assert response.status_code == 302
        assert Post.objects.last().title == "new_post"
        assert Post.objects.last().content == "new post content"

    def test_post_create_view_fail(self, client):
        client.login(username="test_user", password="test12345")
        response = client.post(reverse("post-create"), {})
        assert response.status_code == 200
        assert "This field is required." in str(response.content)

    def test_post_delete_view(self, client, post):
        client.login(username="test_user", password="test12345")
        response = client.post(reverse("post-delete", kwargs={"pk": post.pk}))
        assert response.status_code == 302
        assert not Post.objects.first()

    def test_user_posts_view(self, client):
        client.login(username="test_user", password="test12345")
        response = client.get(reverse("user-posts", kwargs={"username": "test_user"}))
        assert response.status_code == 200
        assert "Posts by test_user (1)" in str(response.content)
        assert response.context[0]["posts"].count() == 1
        assert response.context[0]["page_obj"].number == 1


@pytest.mark.django_db
class TestCommentView:
    @pytest.fixture(name="user", scope="class")
    def create_user(self, django_db_blocker, django_db_setup):
        with django_db_blocker.unblock():
            user = User.objects.create_user(
                username="test_user", email="test@demo.pl", password="test12345"
            )
        yield user
        with django_db_blocker.unblock():
            user.delete()

    @pytest.fixture(name="post", scope="class")
    def create_post(self, django_db_blocker, django_db_setup, user):
        with django_db_blocker.unblock():
            post = Post.objects.create(
                title="Test post", content="Test content", author=user
            )
        yield post
        with django_db_blocker.unblock():
            post.delete()

    @pytest.fixture(name="comment", scope="class")
    def create_comment(self, django_db_blocker, django_db_setup, user, post):
        with django_db_blocker.unblock():
            comment = Comment.objects.create(
                content="Test content", author=user, post=post
            )
        yield comment
        with django_db_blocker.unblock():
            comment.delete()

    def test_comment_view(self, client, post):
        client.login(username="test_user", password="test12345")
        response = client.post(
            reverse("comment-create", kwargs={"pk": post.pk}),
            {"content": "test comment content", "post": post},
        )
        assert response.status_code == 302
        assert post.comments.count() == 1
        assert post.comments.all()[0].content == "test comment content"
        assert post.comments.all()[0].author.username == "test_user"

    def test_comment_update_view(self, client, post, comment):
        client.login(username="test_user", password="test12345")
        response = client.post(
            reverse("comment-update", kwargs={"pk": comment.pk}),
            {"content": "Test content 123", "post": post},
        )
        assert response.status_code == 302
        assert post.comments.all()[0].content == "Test content 123"

    def test_comment_delete_view(self, client, post, comment):
        client.login(username="test_user", password="test12345")
        response = client.post(reverse("comment-delete", kwargs={"pk": comment.pk}))
        assert response.status_code == 302
        assert post.comments.count() == 0


@pytest.mark.django_db
class TestLikeView:
    @pytest.fixture(name="post", scope="class")
    def create_post(self, django_db_blocker, django_db_setup):
        with django_db_blocker.unblock():
            user = User.objects.create_user(
                username="test_user", email="test@demo.pl", password="test12345"
            )
            user.save()
            post = Post.objects.create(
                title="Test post", content="Test content", author=user
            )
            post.save()
        yield post
        with django_db_blocker.unblock():
            post.delete()
            user.delete()

    def test_like_view(self, post, client):
        client.login(username="test_user", password="test12345")
        response = client.post(
            reverse("like-post", kwargs={"pk": post.pk}), {"post_id": post.pk}
        )
        assert response.status_code == 302
        assert post.likes.count() == 1
