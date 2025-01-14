# Generated by Django 5.0.6 on 2024-07-05 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asset_Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Category Name')),
                ('required_file_types', models.CharField(max_length=400, verbose_name='Required File Types')),
                ('min_asset_size', models.DecimalField(decimal_places=2, max_digits=3, verbose_name='Minimum Asset Size')),
                ('max_asset_size', models.DecimalField(decimal_places=2, max_digits=3, verbose_name='Maximum Asset Size')),
            ],
            options={
                'verbose_name': 'Asset Category',
                'verbose_name_plural': 'Asset Categories',
                'ordering': ['name'],
            },
        ),
    ]
