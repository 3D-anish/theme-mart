# Generated by Django 5.0.6 on 2024-07-26 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0021_asset_category_slug_alter_asset_preview_images_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset_category',
            name='slug',
            field=models.SlugField(unique=True, verbose_name=' Slug'),
        ),
    ]