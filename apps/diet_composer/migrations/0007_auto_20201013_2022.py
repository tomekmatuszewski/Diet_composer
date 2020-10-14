# Generated by Django 3.1 on 2020-10-13 20:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("diet_composer", "0006_auto_20201012_1009"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="product",
            options={"ordering": ("category", "name")},
        ),
        migrations.AlterModelOptions(
            name="productcategory",
            options={"ordering": ("name",)},
        ),
        migrations.AddField(
            model_name="product",
            name="author",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="products",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="name",
            field=models.CharField(max_length=150, unique=True),
        ),
        migrations.AlterField(
            model_name="productcategory",
            name="name",
            field=models.CharField(max_length=150, unique=True),
        ),
    ]
