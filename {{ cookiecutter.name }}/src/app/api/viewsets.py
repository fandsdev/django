from typing import Any, Optional, Protocol, Type

from rest_framework import mixins, status
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import GenericViewSet

__all__ = ["DefaultModelViewSet"]


class BaseGenericViewSet(Protocol):
    def get_serializer(self, *args: Any, **kwargs: Any) -> Any: ...

    def get_response(self, *args: Any, **kwargs: Any) -> Any: ...

    def perform_create(self, *args: Any, **kwargs: Any) -> Any: ...

    def perform_update(self, *args: Any, **kwargs: Any) -> Any: ...

    def get_success_headers(self, *args: Any, **kwargs: Any) -> Any: ...

    def get_serializer_class(self, *args: Any, **kwargs: Any) -> Any: ...

    def get_object(self, *args: Any, **kwargs: Any) -> Any: ...


class DefaultCreateModelMixin(CreateModelMixin):
    """Return detail-serialized created instance"""

    def create(self: BaseGenericViewSet, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)  # No getting created instance in original DRF
        headers = self.get_success_headers(serializer.data)
        return self.get_response(instance, status.HTTP_201_CREATED, headers)

    def perform_create(self: BaseGenericViewSet, serializer: Any) -> Any:
        return serializer.save()  # No returning created instance in original DRF


class DefaultUpdateModelMixin(UpdateModelMixin):
    """Return detail-serialized updated instance"""

    def update(self: BaseGenericViewSet, request: Request, *args: Any, **kwargs: Any) -> Response:
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_update(serializer)  # No getting updated instance in original DRF

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return self.get_response(instance, status.HTTP_200_OK)

    def perform_update(self: BaseGenericViewSet, serializer: Any) -> Any:
        return serializer.save()  # No returning updated instance in original DRF


class ResponseWithRetrieveSerializerMixin:
    """
    Always response with 'retrieve' serializer or fallback to `serializer_class`.
    Usage:

    class MyViewSet(DefaultModelViewSet):
        serializer_class = MyDefaultSerializer
        serializer_action_classes = {
           'list': MyListSerializer,
           'my_action': MyActionSerializer,
        }
        @action
        def my_action:
            ...

    'my_action' request will be validated with MyActionSerializer,
    but response will be serialized with MyDefaultSerializer
    (or 'retrieve' if provided).

    Thanks gonz: http://stackoverflow.com/a/22922156/11440

    """

    def get_response(
        self: BaseGenericViewSet,
        instance: Any,
        status: Any,
        headers: Any = None,
    ) -> Response:
        retrieve_serializer_class = self.get_serializer_class(action="retrieve")
        context = self.get_serializer_context()  # type: ignore
        retrieve_serializer = retrieve_serializer_class(instance, context=context)
        return Response(
            retrieve_serializer.data,
            status=status,
            headers=headers,
        )

    def get_serializer_class(
        self: BaseGenericViewSet,
        action: Optional[str] = None,
    ) -> Type[BaseSerializer]:
        if action is None:
            action = self.action  # type: ignore

        try:
            return self.serializer_action_classes[action]  # type: ignore
        except (KeyError, AttributeError):
            return super().get_serializer_class()  # type: ignore[safe-super]


class DefaultModelViewSet(
    DefaultCreateModelMixin,  # Create response is overriden
    mixins.RetrieveModelMixin,
    DefaultUpdateModelMixin,  # Update response is overriden
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    ResponseWithRetrieveSerializerMixin,  # Response with retrieve or default serializer
    GenericViewSet,
):
    pass


class ReadonlyModelViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    ResponseWithRetrieveSerializerMixin,  # Response with retrieve or default serializer
    GenericViewSet,
):
    pass


class ListOnlyModelViewSet(
    mixins.ListModelMixin,
    ResponseWithRetrieveSerializerMixin,  # Response with retrieve or default serializer
    GenericViewSet,
):
    pass


class UpdateOnlyModelViewSet(
    DefaultUpdateModelMixin,
    ResponseWithRetrieveSerializerMixin,
    GenericViewSet,
):
    pass


class DefaultRetrieveDestroyListViewSet(
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    ResponseWithRetrieveSerializerMixin,  # Response with retrieve or default serializer
    GenericViewSet,
):
    pass


class ListUpdateModelViewSet(
    DefaultUpdateModelMixin,
    mixins.ListModelMixin,
    ResponseWithRetrieveSerializerMixin,
    GenericViewSet,
):
    pass
