from typing import Union

from django.core.exceptions import ImproperlyConfigured
from django.db.models import QuerySet
from django.http import QueryDict


class AnnotateForOrderingMixin:
    """Annotate queryset for ordering when it needs to.

    It helps to avoid annotations (that may be heavy) for ordering filter in viewset's `get_queryset`.
    Instead of that you can declare `annotate_for_ordering_{ordering_param_name}` methods in FilterSet
    class: the annotation will happen only when the ordering filter's param is used in the request's query params.

    Example of use (see tests for more):
        class SomeFilterSet(AnnotateForOrderingMixin, filters.FilterSet):
            ordering = filters.OrderingFilter(
                fields=('score'),  <-- ordering param that requires annotation
            )

            def annotate_for_ordering_by_score(self, queryset):  <-- will be called when `?ordering=score` in request
                return queryset.do_heavy_annotation()

    N.B.:
        1. Default ordering filter name: `ordering`.
        You can set it explicitly with `ordering_filter_name` attribute

        2. To annotate queryset for ordering by `param_name` declare
            `def annotate_for_ordering_by_{param_name}(self, queryset: Queryset) -> Queryset:`
        method.
    """

    ordering_filter_name: str = 'ordering'

    def filter_queryset(self, queryset: QuerySet) -> QuerySet:
        self.validate_ordering_filter_name()
        queryset = self.annotate_for_ordering(queryset, self.get_ordering_params(self.data))  # type: ignore

        return super().filter_queryset(queryset)  # type: ignore

    def validate_ordering_filter_name(self) -> None:
        if not self.declared_filters.get(self.ordering_filter_name):  # type: ignore
            raise ImproperlyConfigured(
                f'Ordering filter \"{self.ordering_filter_name}\" was not found. '
                'Set filter with default name `ordering` or use `ordering_filter_name` attr.',
            )

    def get_ordering_params(self, data: Union[QueryDict, None]) -> set[str]:
        if data is None:
            return set()

        request_ordering_query = data.get(self.ordering_filter_name)
        if not request_ordering_query:
            return set()

        return {
            param[1:] if param.startswith('-') else param
            for param in request_ordering_query.split(',')
        }

    def annotate_for_ordering(self, queryset: QuerySet, ordering_params: set[str]) -> QuerySet:
        for param in ordering_params:
            method = getattr(self, f'annotate_for_ordering_by_{param}', None)
            queryset = method(queryset) if method else queryset

        return queryset
