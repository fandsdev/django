from django.db import models

from app.models import DefaultModel


class Sepulka(DefaultModel):
    title = models.CharField(max_length=255)
    image = models.ImageField()

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.title
