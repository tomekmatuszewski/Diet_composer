from django.db import models
from apps.diet_composer.utils import calculate_params


class ProductCategory(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.name}",


class Product(models.Model):

    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT, related_name="products")
    name = models.CharField(max_length=150)
    calories_per_100 = models.DecimalField(max_digits=6, decimal_places=2)
    proteins_per_100 = models.DecimalField(max_digits=6, decimal_places=2)
    fats_per_100 = models.DecimalField(max_digits=6, decimal_places=2)
    carbohydrates_per_100 = models.DecimalField(max_digits=6, decimal_places=2)
    weight_of_pcs = models.DecimalField(null=True, blank=True, max_digits=6, decimal_places=2,
                                        help_text="weight of an average piece / package")

    def __str__(self):
        return f"{self.name}"


class ProductItem(models.Model):
    class Unit(models.TextChoices):
        gram = 'g'
        piece = 'piece'
        package = 'package'
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    unit = models.CharField(choices=Unit.choices, null=True, blank=True, max_length=150)
    weight = models.DecimalField(max_digits=6, decimal_places=2, help_text="Depends on "
                                                                           "selected unit - grams or piece/package")

    def __str__(self):
        return f"{self.product.name} item"

    @property
    def calories(self):
        calories = calculate_params(self.unit, self.product.calories_per_100,
                                    self.weight, self.product.weight_of_pcs)
        return calories

    @property
    def proteins(self):
        proteins = calculate_params(self.unit, self.product.proteins_per_100,
                                    self.weight, self.product.weight_of_pcs)
        return proteins

    @property
    def fats(self):
        fats = calculate_params(self.unit, self.product.fats_per_100,
                                    self.weight, self.product.weight_of_pcs)
        return fats

    @property
    def carbohydrates(self):
        carb = calculate_params(self.unit, self.product.carbohydrates_per_100,
                                self.weight, self.product.weight_of_pcs)
        return carb


