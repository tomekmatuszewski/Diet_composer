import pytest

from apps.users.forms import UserRegisterForm


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
