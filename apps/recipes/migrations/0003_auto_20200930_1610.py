# Generated by Django 3.1 on 2020-09-30 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_recipe_likes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='preparing_time',
            new_name='preparation_time',
        ),
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(default='default_recipe.png', upload_to='recipes_pics'),
        ),
    ]
