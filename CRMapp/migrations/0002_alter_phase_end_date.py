# Generated by Django 3.2.15 on 2023-10-09 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CRMapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phase',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Phase Date End'),
        ),
    ]
