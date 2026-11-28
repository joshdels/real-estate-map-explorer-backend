from django.urls import path

from .views import PropertyImageUploadView

app_name = "media_uploads"
urlpatterns = [path("images", PropertyImageUploadView.as_view(), name="property-image")]
