# Generated by Django 3.2.15 on 2023-12-08 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CRMapp', '0005_pdfmaintenancecontract'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pdfmaintenancecontract',
            name='file',
            field=models.FileField(blank=True, upload_to=''),
        ),
    ]
