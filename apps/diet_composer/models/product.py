from django.contrib.auth.models import User
from django.db import models

from apps.diet_composer.utils import calculate_params


class ProductCategory(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ("name",)


class Product(models.Model):

    category = models.ForeignKey(
        ProductCategory, on_delete=models.PROTECT, related_name="products"
    )
    name = models.CharField(max_length=150, unique=True)
    calories_per_100 = models.DecimalField(max_digits=6, decimal_places=2)
    proteins_per_100 = models.DecimalField(max_digits=6, decimal_places=2)
    fats_per_100 = models.DecimalField(max_digits=6, decimal_places=2)
    carbohydrates_per_100 = models.DecimalField(max_digits=6, decimal_places=2)
    weight_of_pcs = models.DecimalField(
        null=True,
        blank=True,
        max_digits=6,
        decimal_places=2,
        help_text="weight of an average piece / package [g]",
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")

    class Meta:
        ordering = ("category", "name")

    def __str__(self):
        if self.weight_of_pcs:
            return f"{self.name}, weight of piece/packege {self.weight_of_pcs} g"
        return f"{self.name}"


class ProductItem(models.Model):
    class Unit(models.TextChoices):
        gram = "g"
        piece = "piece"
        package = "package"

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.CASCADE,
        related_name="prod_items",
        null=True,
        blank=True,
    )
    unit = models.CharField(choices=Unit.choices, null=True, blank=True, max_length=150)
    weight = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        help_text="Depends on " "selected unit - grams or piece/package",
    )

    def __str__(self):
        return f"Ingredient: {self.product.name}, {self.weight_of_pcs} g"

    @property
    def weight_of_pcs(self) -> float:
        if self.unit == "g":
            return self.weight
        return round(self.product.weight_of_pcs * self.weight, 1)

    @property
    def calories(self) -> float:
        calories = calculate_params(
            self.unit,
            self.product.calories_per_100,
            self.weight,
            self.product.weight_of_pcs,
        )
        return calories

    @property
    def proteins(self) -> float:
        proteins = calculate_params(
            self.unit,
            self.product.proteins_per_100,
            self.weight,
            self.product.weight_of_pcs,
        )
        return proteins

    @property
    def fats(self) -> float:
        fats = calculate_params(
            self.unit,
            self.product.fats_per_100,
            self.weight,
            self.product.weight_of_pcs,
        )
        return fats

    @property
    def carbohydrates(self) -> float:
        carb = calculate_params(
            self.unit,
            self.product.carbohydrates_per_100,
            self.weight,
            self.product.weight_of_pcs,
        )
        return carb
