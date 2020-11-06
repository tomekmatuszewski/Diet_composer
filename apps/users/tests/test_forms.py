import pytest

from apps.users.forms import ProfileUpdateForm, UserRegisterForm, UserUpdateForm


@pytest.mark.django_db
class TestForms:
    def test_user_valid_data(self):
        form = UserRegisterForm(
            data={
                "username": "test_user",
                "email": "test@gmail.com",
                "password1": "test12345",
                "password2": "test12345",
            }
        )
        assert form.is_valid()

    def test_user_not_valid_data(self):
        form = UserRegisterForm(
            data={
                "username": "test_user",
                "email": "test@gmail.com",
                "password1": "test",
                "password2": "test",
            }
        )
        assert not form.is_valid()
        assert len(form.errors) == 1

    def test_user_not_valid_data_empty(self):
        form = UserRegisterForm(data={})
        assert not form.is_valid()
        assert len(form.errors) == 4

    def test_user_update_form(self):
        form = UserUpdateForm(
            data={
                "username": "test_user",
                "email": "test@gmail.com",
            }
        )
        assert form.is_valid()

    def test_profile_update_form(self):
        form = ProfileUpdateForm(
            data={
                "username": "test_user",
                "email": "test@gmail.com",
                "image": "media/default.jpg",
            }
        )
        assert form.is_valid()
