# Generated by Django 3.2.15 on 2023-12-09 11:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CRMapp', '0007_alter_pdfmaintenancecontract_maintenance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pdfmaintenancecontract',
            name='maintenance',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='CRMapp.maintenance'),
        ),
    ]
