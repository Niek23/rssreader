# Generated by Django 3.2.5 on 2021-07-07 09:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0005_tasks'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Tasks',
        ),
    ]