# Generated by Django 3.0.8 on 2020-08-12 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorial', '0011_auto_20200812_1124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutorial',
            name='question_link',
            field=models.URLField(default='https://YoumaykeepitBlank.com/'),
        ),
    ]
