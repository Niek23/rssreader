# Generated by Django 3.2.5 on 2021-07-08 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0010_alter_article_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='feed',
            name='updating',
            field=models.BooleanField(default=True),
        ),
    ]
