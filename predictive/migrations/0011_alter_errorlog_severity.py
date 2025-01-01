# Generated by Django 5.1.4 on 2025-01-01 11:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predictive', '0010_errorlog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='errorlog',
            name='severity',
            field=models.IntegerField(help_text='severity must be between 1 to 10 ( integer ) ', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)]),
        ),
    ]