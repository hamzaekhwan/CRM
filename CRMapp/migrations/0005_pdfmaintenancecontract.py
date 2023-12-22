# Generated by Django 3.2.15 on 2023-12-08 11:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CRMapp', '0004_auto_20231202_1145'),
    ]

    operations = [
        migrations.CreateModel(
            name='PdfMaintenanceContract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='')),
                ('maintenance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CRMapp.maintenance')),
            ],
        ),
    ]