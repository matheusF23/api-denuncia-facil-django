# Generated by Django 3.0.6 on 2020-11-10 00:24

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('guards', '0002_auto_20201109_2011'),
        ('occurrences', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Ocurrence',
            new_name='Occurrence',
        ),
    ]
