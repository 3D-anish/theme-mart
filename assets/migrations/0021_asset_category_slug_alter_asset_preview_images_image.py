# Generated by Django 5.0.6 on 2024-07-26 05:42

import assets.helper_func
import django_resized.forms
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0020_alter_asset_preview_images_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset_category',
            name='slug',
            field=models.SlugField(default='name', verbose_name=' Slug'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='asset_preview_images',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=['middle', 'center'], force_format=None, keep_meta=True, quality=95, scale=None, size=[720, 923], upload_to=assets.helper_func.get_asset_preview_image_path, verbose_name='Preview Image'),
        ),
    ]
