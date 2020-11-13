from datetime import date

from django.db import models

from apps.guards.models import Guard
from denunciafacilapi import settings


class Occurrence(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True,
                             verbose_name='nome usuário')
    guard = models.ForeignKey(Guard, on_delete=models.PROTECT, blank=True, null=True,
                              verbose_name='guarda')
    license_plate = models.CharField(max_length=10, blank=True, null=True, verbose_name='placa veículo')
    occurrence_type = models.CharField(max_length=50, blank=True, null=True, verbose_name='tipo')
    occurrence_title = models.CharField(max_length=255, blank=True, null=True, verbose_name='título')
    location = models.CharField(max_length=400, blank=True, null=True, verbose_name='localização')
    observation = models.CharField(max_length=400, blank=True, null=True, verbose_name='observação')
    anonymous = models.BooleanField(default=False, verbose_name='denúncia anônima')
    image = models.ImageField(upload_to='occurrences', blank=True, null=True, verbose_name='imagem')

    STATUS_CHOICES = [
        (0, 'Enviado'),
        (1, 'Recebido'),
    ]
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    created_at = models.DateField(default=date.today, verbose_name='data')

    class Meta:
        verbose_name = 'ocorrência'
        verbose_name_plural = 'ocorrências'
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.occurrence_title}'
