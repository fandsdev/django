from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    remote_addr = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'remote_addr',
        ]

    def get_remote_addr(self, obj: User) -> str:
        return self.context['request'].META['REMOTE_ADDR']
