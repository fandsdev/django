from ipware import get_client_ip


def real_ip_middleware(get_response):
    """Set request.META['REMOTE_ADDR'] to ip guessed by django-ipware.

    We need this to make sure all apps using ip detection in django way stay usable behind
    any kind of reverse proxy.

    For custom proxy configuration check out django-ipware docs at https://github.com/un33k/django-ipware
    """
    def middleware(request):
        request.META['REMOTE_ADDR'] = get_client_ip(request)[0]

        return get_response(request)

    return middleware
