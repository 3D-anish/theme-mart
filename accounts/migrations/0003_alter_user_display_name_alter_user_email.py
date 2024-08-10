# Generated by Django 5.0.6 on 2024-07-13 08:59

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_is_seller'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='display_name',
            field=models.CharField(blank=True, error_messages={'max_length': 'Name is too long, max - 50.'}, max_length=50, null=True, verbose_name='Display Name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(error_messages={'unique': 'Email ID is already register, try login'}, help_text='Only for security reasons', max_length=254, unique=True, validators=[django.core.validators.EmailValidator], verbose_name='Email Id'),
        ),
    ]