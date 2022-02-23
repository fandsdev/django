import json
import random
import string
from typing import Optional

from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient as DRFAPIClient

from users.models import User


class ApiClient(DRFAPIClient):
    def __init__(self, user: Optional[User] = None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        if user:
            self.user = user
            self.password = ''.join([random.choice(string.hexdigits) for _ in range(6)])
            self.user.set_password(self.password)
            self.user.save()

            token = Token.objects.create(user=self.user)
            self.credentials(
                HTTP_AUTHORIZATION=f'Token {token}',
                HTTP_X_CLIENT='testing',
            )

    def get(self, *args, **kwargs):
        expected_status = kwargs.get('expected_status', 200)
        return self._request('get', expected_status, *args, **kwargs)

    def patch(self, *args, **kwargs):
        expected_status = kwargs.get('expected_status', 200)
        return self._request('patch', expected_status, *args, **kwargs)

    def post(self, *args, **kwargs):
        expected_status = kwargs.get('expected_status', 201)
        return self._request('post', expected_status, *args, **kwargs)

    def put(self, *args, **kwargs):
        expected_status = kwargs.get('expected_status', 200)
        return self._request('put', expected_status, *args, **kwargs)

    def delete(self, *args, **kwargs):
        expected_status = kwargs.get('expected_status', 204)
        return self._request('delete', expected_status, *args, **kwargs)

    def _request(self, method, expected, *args, **kwargs):
        kwargs['format'] = kwargs.get('format', 'json')
        as_response = kwargs.pop('as_response', False)
        method = getattr(super(), method)

        response = method(*args, **kwargs)
        if as_response:
            return response

        content = self._decode(response)
        assert response.status_code == expected, content
        return content

    def _decode(self, response):
        content = response.content.decode('utf-8', errors='ignore')

        if self.is_json(response):
            return json.loads(content)
        else:
            return content

    @staticmethod
    def is_json(response) -> bool:
        if response.has_header('content-type'):
            return 'json' in response.get('content-type')

        return False


__all__ = [
    'ApiClient',
]
