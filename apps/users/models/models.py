from django.contrib.auth.models import User
from django.db import models

from apps.users.utils import (calc_daily_carb, calc_daily_fats,
                              calc_daily_proteins, calculate_bmr,
                              calculate_cmr, change_pic_size, validate_age)


class UserActivity(models.Model):
    description = models.CharField(max_length=150)
    factor = models.FloatField()

    def __str__(self):
        return f"{self.description}, factor: {self.factor}"


class Profile(models.Model):
    class Gender(models.TextChoices):
        Male = "Male"
        Female = "Female"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    image = models.ImageField(default="default.jpg", upload_to="profile_pics")
    age = models.PositiveSmallIntegerField(
        validators=[validate_age], null=True, blank=True
    )
    gender = models.CharField(
        choices=Gender.choices, max_length=10, null=True, blank=True
    )
    height = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
        help_text="height in centimeters",
    )
    weight = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
        help_text="weight in kilograms",
    )
    activity = models.ForeignKey(
        UserActivity, on_delete=models.PROTECT, null=True, blank=True
    )

    def __str__(self) -> str:
        return f"{self.user.username} profile"

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)
        change_pic_size(self.image.path, 300, 300)

    @property
    def bmr(self):
        return calculate_bmr(self.weight, self.height, self.age, self.gender)

    @property
    def cmr(self):
        return calculate_cmr(self.bmr, self.activity.factor)

    @property
    def daily_proteins(self):
        return calc_daily_proteins(self.cmr)

    @property
    def daily_fats(self):
        return calc_daily_fats(self.cmr)

    @property
    def daily_carb(self):
        return calc_daily_carb(self.cmr)
