import pytest

from django_filters import rest_framework as filters

from django.core.exceptions import ImproperlyConfigured
from django.db import models

from app.api.filterset_mixins import AnnotateForOrderingMixin


class DummyQuerySet(models.QuerySet):
    def do_heavy_annotation(self):
        return self

    def order_by(self, *field_names):
        return self


class DummyModel(models.Model):
    objects = DummyQuerySet.as_manager()

    class Meta:
        app_label = 'dummy_app'

    def __str__(self):
        pass


class FilterSetDeclaredOrdering(AnnotateForOrderingMixin, filters.FilterSet):
    ordering = filters.OrderingFilter(
        fields=(
            'color',  # common model field
            'score',  # require heavy annotation
        ),
    )

    def annotate_for_ordering_by_score(self, queryset):  # should be called for ordering by `score` field
        return queryset.do_heavy_annotation()


class FilterSetNotDeclaredOrdering(AnnotateForOrderingMixin, filters.FilterSet):
    pass


class FilterSetDeclaredNonDefaultOrdering(AnnotateForOrderingMixin, filters.FilterSet):
    ordering_filter_name = 'non_default_ordering'

    non_default_ordering = filters.OrderingFilter(
        fields=(
            'color',
            'score',
        ),
    )

    def annotate_for_ordering_by_color(self, queryset):  # should be called for ordering by `color` field
        return queryset.do_heavy_annotation()


@pytest.fixture
def queryset():
    return DummyModel.objects.none()  # none() is enough for tests and not trying to access to db


@pytest.fixture
def get_filterset(queryset):
    return (
        lambda _data, _queryset=queryset, filterset_class=FilterSetDeclaredOrdering:
        filterset_class(data=_data, queryset=_queryset)
    )


@pytest.fixture
def spy_heavy_annotation(mocker):
    return mocker.spy(DummyQuerySet, 'do_heavy_annotation')


@pytest.fixture
def spy_order_by(mocker):
    return mocker.spy(DummyQuerySet, 'order_by')


def test_queryset_annotation_called_while_ordering_by_field_with_annotate_for_method(get_filterset, spy_heavy_annotation):
    data = {
        'ordering': 'score',
    }

    get_filterset(data).qs  # act

    spy_heavy_annotation.assert_called_once()


def test_annotate_for_ordering_not_called_common_field(get_filterset, spy_heavy_annotation):
    data = {
        'ordering': 'color',
    }

    get_filterset(data).qs  # act

    spy_heavy_annotation.assert_not_called()


def test_queryset_order_by_called_with_args(get_filterset, spy_heavy_annotation, spy_order_by):
    data = {
        'ordering': 'score,-color',
    }

    get_filterset(data).qs  # act

    spy_heavy_annotation.assert_called_once()
    order_by_field_names = spy_order_by.call_args.args[1:]
    assert order_by_field_names == ('score', '-color')


def test_empty_ordering_request_data_not_call_annotation_and_order_by(get_filterset, spy_heavy_annotation, spy_order_by):
    data = None

    get_filterset(data).qs  # act

    spy_heavy_annotation.assert_not_called()
    spy_order_by.assert_not_called()


def test_improperly_configured_if_ordering_filter_not_declared(get_filterset, queryset):
    data = {
        'ordering': 'score',
    }

    with pytest.raises(ImproperlyConfigured, match='was not found'):
        get_filterset(data, queryset, FilterSetNotDeclaredOrdering).qs


def test_non_default_ordering_field_call_annotation(get_filterset, queryset, spy_heavy_annotation):
    data = {
        'non_default_ordering': 'color',
    }

    get_filterset(data, queryset, FilterSetDeclaredNonDefaultOrdering).qs  # act

    spy_heavy_annotation.assert_called_once()
