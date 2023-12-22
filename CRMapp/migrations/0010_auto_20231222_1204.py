# Generated by Django 3.2.15 on 2023-12-22 09:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CRMapp', '0009_auto_20231211_1516'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='signed',
            field=models.BooleanField(default=False, verbose_name='Signed'),
        ),
        migrations.AlterField(
            model_name='client',
            name='mobile_phone',
            field=models.CharField(max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+9715Xxxxxxxx'.", regex='^\\+9715\\d{7}$')]),
        ),
        migrations.AlterField(
            model_name='maintenance',
            name='helper2',
            field=models.CharField(blank=True, max_length=255, verbose_name='Name Of helper2'),
        ),
    ]