# Generated by Django 3.0.4 on 2020-04-19 09:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pipelines', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pipeline',
            name='delete_date',
            field=models.DateTimeField(null=True, verbose_name='Delete Date'),
        ),
        migrations.AddField(
            model_name='pipeline',
            name='delete_owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='delete_pipeline', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='pipeline',
            name='is_deleted',
            field=models.BooleanField(default=False, verbose_name='Is Deleted'),
        ),
        migrations.AddField(
            model_name='pipeline',
            name='is_obsolete',
            field=models.BooleanField(default=False, verbose_name='Obsolete'),
        ),
    ]
