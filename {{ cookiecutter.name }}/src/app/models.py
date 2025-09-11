from typing import Any

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone


__all__ = [
    "DefaultModel",
    "TimestampedModel",
    "models",
]


class DefaultModel(models.Model):
    class Meta:
        abstract = True

    def __str__(self) -> str:
        """Default name for all models"""
        name = getattr(self, "name", None)
        if name is not None:
            return str(name)

        return super().__str__()

    @classmethod
    def get_contenttype(cls) -> ContentType:
        return ContentType.objects.get_for_model(cls)

    def update(self, **kwargs: "Any") -> "models.Model":
        for key, value in kwargs.items():
            setattr(self, key, value)

        self.save(update_fields=kwargs.keys())

        return self

    @classmethod
    def get_label(cls) -> str:
        """Get a unique within the app model label"""
        return cls._meta.label_lower.split(".")[-1]


class TimestampedModel(DefaultModel):
    """
    Default app model that has `created` and `updated` attributes.
    Custom implementation replacing django-behaviors dependency.
    """

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args: Any, **kwargs: Any) -> Any:
        if self.pk:
            self.updated = timezone.now()
        return super().save(*args, **kwargs)
