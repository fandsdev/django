from copy import copy

from behaviors.behaviors import Timestamped

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import F
from django.db.models.functions import Coalesce

__all__ = [
    'models',
    'DefaultManager',
    'DefaultModel',
    'DefaultQuerySet',
    'TimestampedModel',
]


class DefaultQuerySet(models.QuerySet):
    Q = None  # noqa: VNE001
    """Q is a extension to Django queryset. Defining Q like this:
        class Q:
            @staticmethod
            def delivered():
                return Q(status__extended='delivered')
        Adds the method `delivered` to the queryset (and manager built on it), and
        allows you to reuse the returned Q object, like this:
        class OrderQuerySet:
            class Q:
                @staticmethod
                def delivered():
                    return Q(status__extended='delivered')
            def delivered_yesterday(self):
                return self.filter(self.Q.delivered & Q(delivery_date='2032-12-01'))
    """

    @classmethod
    def as_manager(cls):
        """Copy-paste of stock django as_manager() to use our default manager
        See also: https://github.com/django/django/blob/master/django/db/models/query.py#L198
        """
        manager = DefaultManager.from_queryset(cls)()
        manager._built_with_as_manager = True
        return manager

    as_manager.queryset_only = True

    def __getattr__(self, name):
        if self.Q is not None and hasattr(self.Q, name):
            return lambda *args: self.filter(getattr(self.Q, name)())

        raise AttributeError()

    def with_last_update(self):
        """Annotate `last_update` field that displays the creation or modification date"""
        return self.annotate(last_update=Coalesce(F('modified'), F('created')))


class DefaultManager(models.Manager):
    relations_to_assign_after_creation = []

    def __getattr__(self, name):
        if hasattr(self._queryset_class, 'Q') and hasattr(self._queryset_class.Q, name):
            return getattr(self.get_queryset(), name)

        raise AttributeError(f'Nor {self.__class__}, nor {self._queryset_class.__name__} or {self._queryset_class.__name__}.Q does not have `{name}` defined.')


class DefaultModel(models.Model):
    objects = DefaultManager()

    class Meta:
        abstract = True

    def __str__(self):
        """Default name for all models"""
        if hasattr(self, 'name'):
            return str(self.name)

        return super().__str__()

    @classmethod
    def get_contenttype(cls) -> ContentType:
        return ContentType.objects.get_for_model(cls)

    @classmethod
    def has_field(cls, field) -> bool:
        """
        Shortcut to check if model has particular field
        """
        try:
            cls._meta.get_field(field)
            return True
        except models.FieldDoesNotExist:
            return False

    def update_from_kwargs(self, **kwargs):
        """
        A shortcut method to update model instance from the kwargs.
        """
        for (key, value) in kwargs.items():
            setattr(self, key, value)

    def setattr_and_save(self, key, value):
        """Shortcut for testing -- set attribute of the model and save"""
        setattr(self, key, value)
        self.save()

    def copy(self, **kwargs):
        """Creates new object from current."""
        instance = copy(self)
        kwargs.update({
            'id': None,
            'pk': None,
        })
        instance.update_from_kwargs(**kwargs)
        return instance

    @classmethod
    def get_label(cls) -> str:
        """
        Get a unique within the app model label
        """
        return cls._meta.label_lower.split('.')[-1]


class TimestampedModel(DefaultModel, Timestamped):
    """
    Default app model that has `created` and `updated` attributes.
    Currently based on https://github.com/audiolion/django-behaviors
    """
    class Meta:
        abstract = True
