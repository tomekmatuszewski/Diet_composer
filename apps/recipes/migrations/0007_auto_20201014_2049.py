# Generated by Django 3.1 on 2020-10-14 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0006_auto_20201014_1816"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="name",
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name="recipe",
            name="title",
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
