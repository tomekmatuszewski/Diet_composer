from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    class Unit(models.TextChoices):
        kilogram = 'kg'
        piece = 'piece'

    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT)
    name = models.CharField(max_length=150)
    calories_per_100 = models.DecimalField(max_digits=6, decimal_places=2)
    proteins_per_100 = models.DecimalField(max_digits=6, decimal_places=2)
    fats_per_100 = models.DecimalField(max_digits=6, decimal_places=2)
    carbohydrates_per_100 = models.DecimalField(max_digits=6, decimal_places=2)
    unit = models.CharField(choices=Unit.choices, null=True, blank=True, max_length=150)
    weight_of_pcs = models.DecimalField(null=True, blank=True, max_digits=6, decimal_places=2,
                                        help_text="weight of an average piece / package")

    def __str__(self):
        return f"{self.name}"