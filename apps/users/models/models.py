from django.contrib.auth.models import User
from django.db import models
from apps.users.utils import change_pic_size


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="default.jpg", upload_to="profile_pics")

    def __repr__(self) -> str:
        return f"{self.user.username} Profile"

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)
        change_pic_size(self.image.path)



