from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import ReadOnlyModelViewSet as _ReadOnlyModelViewSet

__all__ = [
    'AppViewSet',
    'ReadOnlyAppViewSet',
]


class MultiSerializerMixin:
    def get_serializer_class(self, action=None):
        """
        Look for serializer class in self.serializer_action_classes, which
        should be a dict mapping action name (key) to serializer class (value),
        i.e.:
        class MyViewSet(MultiSerializerViewSetMixin, ViewSet):
            serializer_class = MyDefaultSerializer
            serializer_action_classes = {
               'list': MyListSerializer,
               'my_action': MyActionSerializer,
            }
            @action
            def my_action:
                ...
        If there's no entry for that action then just fallback to the regular
        get_serializer_class lookup: self.serializer_class, DefaultSerializer.
        Thanks gonz: http://stackoverflow.com/a/22922156/11440
        """
        if action is None:
            action = self.action

        try:
            return self.serializer_action_classes[action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()


class ReadOnlyAppViewSet(MultiSerializerMixin, _ReadOnlyModelViewSet):
    pass


class AppViewSet(MultiSerializerMixin, ModelViewSet):
    """
    This AppViewSet uses MultiSerializerMixin's serializer_action_classes
    to create and update instances with corresponding create and update serializers,
    but always serialize response with serializer_class detail serializer.

    Copy-pasted from DRF create and update mixins with comments near edits.
    """

    def response(self, serializer, instance, status):
        detail_serializer_class = self.get_serializer_class(action='detail')
        detail_serializer = detail_serializer_class(instance)  # Detail-serialize instance
        headers = self.get_success_headers(serializer.data)
        return Response(detail_serializer.data, status=status, headers=headers)

    def create(self, request, *args, **kwargs):
        create_serializer = self.get_serializer(data=request.data)
        create_serializer.is_valid(raise_exception=True)
        instance = self.perform_create(create_serializer)  # Here we grab our created instance
        return self.response(create_serializer, instance, status=status.HTTP_201_CREATED)  # Return detail-serialized created instance

    def perform_create(self, serializer):
        serializer.save()
        return serializer.instance  # Here we return created instance

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        update_serializer = self.get_serializer(instance, data=request.data, partial=partial)
        update_serializer.is_valid(raise_exception=True)
        instance = self.perform_update(update_serializer)  # Here we grab our updated instance

        if getattr(instance, '_prefetched_objects_cache', None):  # ↓ DRF comment
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return self.response(update_serializer, instance, status=status.HTTP_200_OK)  # Return detail-serialized updated instance

    def perform_update(self, serializer):
        serializer.save()
        return serializer.instance  # Here we return updated instance
