# Generated by Django 3.0.6 on 2020-11-09 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guards', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guard',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='nome'),
        ),
    ]