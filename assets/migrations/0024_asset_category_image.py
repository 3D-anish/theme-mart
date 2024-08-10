# Generated by Django 5.0.6 on 2024-07-28 19:38

import assets.helper_func
import django_resized.forms
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0023_alter_asset_preview_images_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset_category',
            name='image',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, keep_meta=True, null=True, quality=100, scale=None, size=[1920, 1080], upload_to=assets.helper_func.get_asset_category_image_path, verbose_name='Asset Category Image'),
        ),
    ]