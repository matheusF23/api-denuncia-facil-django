# Generated by Django 3.0.6 on 2020-11-13 22:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('occurrences', '0006_occurrence_anonymous'),
    ]

    operations = [
        migrations.AlterField(
            model_name='occurrence',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='nome usuário'),
        ),
    ]
