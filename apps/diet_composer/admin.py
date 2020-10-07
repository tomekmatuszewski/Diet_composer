from django.contrib import admin
from apps.diet_composer.models import Product, ProductCategory, ProductItem, Meal, DailyMenu

admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(ProductItem)
admin.site.register(Meal)
admin.site.register(DailyMenu)
