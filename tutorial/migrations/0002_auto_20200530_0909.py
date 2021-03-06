# Generated by Django 3.0.6 on 2020-05-30 03:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tutorial', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutorial',
            name='owner',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='topics',
            name='topic_name',
            field=models.CharField(max_length=30),
        ),
    ]
