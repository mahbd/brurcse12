# Generated by Django 3.0.8 on 2020-08-12 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorial', '0009_auto_20200609_1257'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tutorial',
            old_name='tut_title',
            new_name='title',
        ),
        migrations.AlterField(
            model_name='tutorial',
            name='question_link',
            field=models.URLField(blank=True, null=True),
        ),
    ]
