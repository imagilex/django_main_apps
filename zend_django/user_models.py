from django.db import models

from django.contrib.auth.models import User


class UserProfile(models.Model):
    apellido_materno = models.CharField(max_length=50, blank=True)
    telefono = models.CharField(max_length=10, blank=True)
    celular = models.CharField(max_length=10, blank=True)
    whatsapp = models.CharField(
        max_length=10, blank=True, verbose_name="what's App")
    user = models.OneToOneField(
        to=User, on_delete=models.CASCADE, related_name="profile")

    class Meta:
        ordering = ['telefono', 'celular', 'whatsapp']

    def __str__(self):
        return f"{self.user}"
