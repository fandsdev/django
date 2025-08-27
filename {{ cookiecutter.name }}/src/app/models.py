from typing import Any

from behaviors.behaviors import Timestamped  # type: ignore[import-untyped]
from django.contrib.contenttypes.models import ContentType
from django.db import models


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
        
    def update(self, **kwargs: "Any") -> "models.Model":  # type: ignore[misc]
        for key, value in kwargs.items():
            setattr(self, key, value)

        self.save(update_fields=kwargs.keys())

        return self
        
    @classmethod
    def get_label(cls) -> str:
        """Get a unique within the app model label"""
        return cls._meta.label_lower.split(".")[-1]


class TimestampedModel(DefaultModel, Timestamped):
    """
    Default app model that has `created` and `updated` attributes.
    Currently based on https://github.com/audiolion/django-behaviors
    """

    class Meta:
        abstract = True
