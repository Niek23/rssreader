# Generated by Django 3.2.5 on 2021-07-06 10:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('feed', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='feed',
            old_name='name',
            new_name='title',
        ),
        migrations.AddField(
            model_name='feed',
            name='subscribers',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='subscriber'),
        ),
        migrations.AddField(
            model_name='feed',
            name='subtitle',
            field=models.CharField(default='No subtitle', max_length=150),
        ),
    ]