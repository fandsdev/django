from collections.abc import Iterable
from typing import Any

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.base import ModelBase
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
    Default app model that has `created` and `modified` attributes.
    """

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def save(
        self,
        *,
        force_insert: bool | tuple[ModelBase, ...] = False,
        force_update: bool = False,
        using: str | None = None,
        update_fields: Iterable[str] | None = None,
    ) -> None:
        if self.pk:
            self.modified = timezone.now()
        return super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )
