# Generated by Django 5.0.6 on 2024-08-01 22:16

import main.helper_func
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HomeBanner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banner', models.ImageField(upload_to=main.helper_func.get_home_banner_path, verbose_name='Banner')),
                ('link', models.URLField(verbose_name='URL')),
                ('h1_title', models.CharField(blank=True, max_length=100, null=True, verbose_name='H1 Title')),
                ('h4_title', models.CharField(blank=True, max_length=100, null=True, verbose_name='H4 Title')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Home Banner',
                'verbose_name_plural': 'Home Banners',
                'ordering': ['-date_created'],
            },
        ),
    ]
