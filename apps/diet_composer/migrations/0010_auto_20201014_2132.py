# Generated by Django 3.1 on 2020-10-14 21:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("diet_composer", "0009_auto_20201014_2049"),
    ]

    operations = [
        migrations.RenameField(
            model_name="recipeitem",
            old_name="category",
            new_name="recipe_category",
        ),
    ]