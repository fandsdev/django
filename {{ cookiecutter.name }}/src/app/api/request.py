from rest_framework.request import Request

from users.models import User


class AuthenticatedRequest(Request):
    user: User
