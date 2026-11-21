from django.urls import path

from .views import DatasetView

app_name = "datasets"
urlpatterns = [path("dataset", DatasetView.as_view(), name="dataset")]
