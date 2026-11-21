from django.conf import settings
from django.urls import include, path

app_name = "accounts"
urlpatterns = [
    path("", include("dj_rest_auth.urls")),
    path("registration/", include("dj_rest_auth.registration.urls")),
]

if settings.ENABLE_SOCIAL_AUTH:
    from .views import FacebookLogin, GoogleLogin

    urlpatterns += [
        path("google/", GoogleLogin.as_view(), name="google-login"),
        path("facebook/", FacebookLogin.as_view(), name="facebook-login"),
    ]
