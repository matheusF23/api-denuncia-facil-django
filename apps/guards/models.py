from django.db import models


class Guard(models.Model):
    cod_guard = models.CharField(max_length=20, unique=True, verbose_name='códido do guarda')
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name='nome')

    class Meta:
        verbose_name = 'guarda'
        verbose_name_plural = 'guardas'

    def __str__(self):
        return self.name
