# Generated by Django 3.0.6 on 2020-11-13 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('occurrences', '0008_auto_20201113_1903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='occurrence',
            name='anonymous',
            field=models.BooleanField(default=False, verbose_name='denúncia anônima'),
        ),
    ]
