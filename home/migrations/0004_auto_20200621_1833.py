# Generated by Django 3.0.7 on 2020-06-21 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_announce'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announce',
            name='ann_title',
            field=models.CharField(max_length=30),
        ),
    ]
