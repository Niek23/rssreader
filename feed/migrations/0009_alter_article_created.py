# Generated by Django 3.2.5 on 2021-07-08 10:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0008_auto_20210707_1435'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='created',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]
