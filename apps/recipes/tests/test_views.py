import os
from pathlib import Path

import pytest
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from apps.recipes.models import Category, Recipe

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent.parent


@pytest.mark.django_db
class TestRecipeView:
    @pytest.fixture(name="user", scope="class")
    def create_user(self, django_db_blocker, django_db_setup):
        with django_db_blocker.unblock():
            user = User.objects.create_user(
                username="test_user", email="test@demo.pl", password="test12345"
            )

        yield user
        with django_db_blocker.unblock():
            user.delete()

    @pytest.fixture(name="recipe", scope="class")
    def create_recipe(self, django_db_blocker, django_db_setup, user):
        with django_db_blocker.unblock():
            category = Category.objects.create(name="cat1")
            recipe = Recipe.objects.create(
                title="Test recipe",
                description="Test description",
                author=user,
                preparation_time="10min",
                ingredients="test ingredients",
                category=category,
            )
        yield recipe
        with django_db_blocker.unblock():
            recipe.delete()

    def test_recipe_view(self, client, recipe, user):
        response = client.get(reverse("diet_composer-recipes"))
        assert response.status_code == 200
        assert "recipes/recipes.html" in [
            template.name for template in response.templates
        ]
        content = str(response.content)
        assert "Test recipe" in content
        assert "/media/default_recipe.png" in content
        assert "Test description" in content
        assert user.username in content

    def test_recipe_create_view(self, client, recipe):
        client.login(username="test_user", password="test12345")
        response = client.post(
            reverse("recipe-create"),
            data={
                "category": recipe.category.id,
                "title": "Test recipe 2",
                "preparation_time": "20 min",
                "description": "Test description 2",
                "ingredients": "test ingredients",
            },
        )
        assert response.status_code == 302
        assert Recipe.objects.count() == 2
        assert Recipe.objects.last().title == "Test recipe 2"
        assert Recipe.objects.last().preparation_time == "20 min"

    def test_recipe_create_view_fail(self, client, recipe):
        client.login(username="test_user", password="test12345")
        response = client.post(reverse("recipe-create"), data={})
        assert response.status_code == 200
        assert Recipe.objects.count() == 1

    def test_recipe_update_view(self, client, recipe):
        image_path = os.path.join(BASE_DIR, "media/test_pics/joker.jpg")
        client.login(username="test_user", password="test12345")
        response = client.post(
            reverse("recipe-update", kwargs={"pk": recipe.pk}),
            data={
                "category": recipe.category.id,
                "title": "Test recipe changed",
                "preparation_time": "40 min",
                "description": "Test description changed",
                "ingredients": "test ingredients changed",
                "image": SimpleUploadedFile(
                    name="joker.jpg",
                    content=open(image_path, "rb").read(),
                    content_type="image/jpg",
                ),
            },
        )
        recipe.refresh_from_db()
        assert response.status_code == 302
        assert Recipe.objects.count() == 1
        assert Recipe.objects.first().title == "Test recipe changed"
        assert Recipe.objects.first().description == "Test description changed"
        assert Recipe.objects.first().image.path == os.path.join(
            BASE_DIR, "media/recipes_pics/joker.jpg"
        )

    def test_recipe_detail_view(self, client, recipe, user):
        response = client.get(reverse("recipe-detail", kwargs={"pk": recipe.pk}))
        assert response.status_code == 200
        assert "recipes/recipe_detail.html" in [
            template.name for template in response.templates
        ]
        content = str(response.content)
        assert "Test recipe" in content
        assert "/media/default_recipe.png" in content
        assert "Test description" in content
        assert response.context["total_likes"] == 0
        assert user.username in content

    def test_recipe_delete_view(self, client, recipe):
        client.login(username="test_user", password="test12345")
        response = client.post(reverse("recipe-delete", kwargs={"pk": recipe.id}))
        assert response.status_code == 302
        assert not Recipe.objects.first()


@pytest.mark.django_db
class TestLikeView:
    @pytest.fixture(name="recipe", scope="class")
    def create_post(self, django_db_blocker, django_db_setup):
        with django_db_blocker.unblock():
            user = User.objects.create_user(
                username="test_user", email="test@demo.pl", password="test12345"
            )
            user.save()
            category = Category.objects.create(name="cat1")
            recipe = Recipe.objects.create(
                title="Test recipe",
                description="Test description",
                author=user,
                preparation_time="10min",
                ingredients="test ingredients",
                category=category,
            )
            recipe.save()
        yield recipe
        with django_db_blocker.unblock():
            recipe.delete()
            user.delete()

    def test_like_view(self, recipe, client):
        client.login(username="test_user", password="test12345")
        response = client.post(
            reverse("recipe-like", kwargs={"pk": recipe.pk}), {"recipe_id": recipe.pk}
        )
        assert response.status_code == 302
        assert recipe.likes.count() == 1
