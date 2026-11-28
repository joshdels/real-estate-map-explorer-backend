import os
from datetime import timedelta
from pathlib import Path

import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "unsafe-local-development-key")
DEBUG = False
ALLOWED_HOSTS = [
    item for item in os.getenv("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",") if item
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.gis",
    "corsheaders",
    "rest_framework",
    "drf_spectacular",
    "rest_framework.authtoken",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.facebook",
    "dj_rest_auth",
    "dj_rest_auth.registration",
    "apps.accounts.apps.AccountsConfig",
    "apps.datasets.apps.DatasetsConfig",
    "apps.media_uploads.apps.MediaUploadsConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "core" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# Lot boundaries are stored as real PostGIS geometry, so the default engine is
# GeoDjango's PostGIS backend. A sqlite fallback keeps `manage.py check` usable
# without a database, but spatial features require PostgreSQL + PostGIS.
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=60,
        conn_health_checks=True,
    )
}
if DATABASES["default"].get("ENGINE") == "django.db.backends.postgresql":
    DATABASES["default"]["ENGINE"] = "django.contrib.gis.db.backends.postgis"
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Manila"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME", "")
if AWS_STORAGE_BUCKET_NAME:
    AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME", "ap-southeast-1")
    AWS_S3_CUSTOM_DOMAIN = os.getenv("AWS_S3_CUSTOM_DOMAIN", "") or None
    AWS_QUERYSTRING_AUTH = False
    AWS_DEFAULT_ACL = None
    AWS_S3_FILE_OVERWRITE = False
    STORAGES = {
        "default": {"BACKEND": "storages.backends.s3.S3Storage"},
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    }
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "accounts.User"
SITE_ID = 1
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*", "password2*"]
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ENABLE_SOCIAL_AUTH = os.getenv("ENABLE_SOCIAL_AUTH", "false").lower() == "true"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ["dj_rest_auth.jwt_auth.JWTCookieAuthentication"],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}
SPECTACULAR_SETTINGS = {
    "TITLE": "Open Lot Plans API",
    "DESCRIPTION": (
        "Django REST API used by the Open Lot Plans Next.js application. "
        "The dataset endpoint is the temporary whole-dataset contract used during migration."
    ),
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}
# The default access token lives only 5 minutes. With the cookie-based flow the
# frontend keeps a visible session far longer, so a short access token made
# authenticated writes (e.g. saving edited lot boundaries) silently fail once it
# expired. Give the access token a usable lifetime and rotate the refresh token.
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
}

REST_AUTH = {
    "USE_JWT": True,
    "JWT_AUTH_COOKIE": "open_lot_access",
    "JWT_AUTH_REFRESH_COOKIE": "open_lot_refresh",
    "JWT_AUTH_HTTPONLY": True,
    "JWT_AUTH_SAMESITE": os.getenv("JWT_AUTH_SAMESITE", "Lax"),
    "JWT_AUTH_SECURE": os.getenv("JWT_AUTH_SECURE", "false").lower() == "true",
    "USER_DETAILS_SERIALIZER": "apps.accounts.serializers.UserSerializer",
}

CORS_ALLOWED_ORIGINS = [
    item for item in os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:3000").split(",") if item
]
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = [
    item for item in os.getenv("CSRF_TRUSTED_ORIGINS", "http://localhost:3000").split(",") if item
]

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {"access_type": "online"},
        "OAUTH_PKCE_ENABLED": True,
    },
    "facebook": {
        "FIELDS": ["id", "email", "name", "first_name", "last_name"],
        "SCOPE": ["email", "public_profile"],
    },
}
for provider, prefix in (("google", "GOOGLE"), ("facebook", "FACEBOOK")):
    client_id = os.getenv(f"{prefix}_OAUTH_CLIENT_ID")
    secret = os.getenv(f"{prefix}_OAUTH_CLIENT_SECRET")
    if client_id and secret:
        SOCIALACCOUNT_PROVIDERS[provider]["APP"] = {
            "client_id": client_id,
            "secret": secret,
            "key": "",
        }
