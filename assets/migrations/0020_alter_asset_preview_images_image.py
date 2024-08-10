# Generated by Django 5.0.6 on 2024-07-23 11:49

import assets.helper_func
import django_resized.forms
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0019_alter_asset_preview_images_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset_preview_images',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=True, quality=95, scale=None, size=[1920, 1080], upload_to=assets.helper_func.get_asset_preview_image_path, verbose_name='Preview Image'),
        ),
    ]