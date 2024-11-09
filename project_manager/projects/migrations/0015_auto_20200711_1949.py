# Generated by Django 3.0.4 on 2020-07-11 18:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0014_auto_20200711_1838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipmentinevent',
            name='equipment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='equipment_event', to='projects.Equipment'),
        ),
    ]
