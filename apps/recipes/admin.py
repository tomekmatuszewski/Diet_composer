from django.contrib import admin

from .models import Category, Recipe

admin.site.register(Recipe)
admin.site.register(Category)
