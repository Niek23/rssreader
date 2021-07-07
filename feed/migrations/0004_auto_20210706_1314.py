# Generated by Django 3.2.5 on 2021-07-06 13:14

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('feed', '0003_auto_20210706_1058'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='is_read_by',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='feed',
            name='subscribers',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]