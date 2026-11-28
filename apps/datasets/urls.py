from django.urls import path

from .views import DatasetView, LotGeometryGeoJSONView

app_name = "datasets"
urlpatterns = [
    path("dataset", DatasetView.as_view(), name="dataset"),
    path("lots.geojson", LotGeometryGeoJSONView.as_view(), name="lots-geojson"),
]
