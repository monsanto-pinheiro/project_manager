# Generated by Django 3.0.4 on 2020-07-03 17:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0004_auto_20200703_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metakeyprojects',
            name='meta_tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='meta_key_project', to='projects.MetaKey'),
        ),
        migrations.AlterField(
            model_name='metakeyprojects',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='meta_key_project', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='metakeyprojects',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='meta_key_project', to='projects.Project'),
        ),
    ]
