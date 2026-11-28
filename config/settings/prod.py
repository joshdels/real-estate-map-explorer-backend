from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa: F403

if SECRET_KEY == "unsafe-local-development-key":  # noqa: F405
    raise ImproperlyConfigured("DJANGO_SECRET_KEY is required in production")
if not AWS_STORAGE_BUCKET_NAME:  # noqa: F405
    raise ImproperlyConfigured("AWS_STORAGE_BUCKET_NAME is required in production")

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
