# Generated by Django 3.2.15 on 2023-11-28 15:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CRMapp', '0007_alter_maintenancelift_contract'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='interest',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CRMapp.interest'),
        ),
        migrations.AlterField(
            model_name='interest',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CRMapp.client'),
        ),
        migrations.AlterField(
            model_name='maintenance',
            name='contract',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CRMapp.contract'),
        ),
        migrations.AlterField(
            model_name='maintenance',
            name='maintenance_lift',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CRMapp.maintenancelift'),
        ),
        migrations.AlterField(
            model_name='maintenancelift',
            name='contract',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='maintenancelift', to='CRMapp.contract'),
        ),
        migrations.AlterField(
            model_name='note',
            name='contract',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CRMapp.contract'),
        ),
        migrations.AlterField(
            model_name='phase',
            name='contract',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CRMapp.contract'),
        ),
    ]