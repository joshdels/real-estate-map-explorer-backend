from django.contrib.gis.db import models as gis_models
from django.db import models


class AppDataset(models.Model):
    payload = models.JSONField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "application dataset"

    def __str__(self):
        return f"Dataset updated {self.updated_at:%Y-%m-%d %H:%M:%S}"


class LotGeometry(gis_models.Model):
    """Normalized PostGIS geometry for a single listing boundary.

    The whole-dataset blob still carries each listing's polygon as JSON during
    the migration, but the authoritative spatial copy lives here so PostGIS can
    index, query, and serve the boundaries as GeoJSON. `listing_id` matches the
    `id` of the listing in the dataset payload.
    """

    listing_id = models.CharField(max_length=120, unique=True)
    title = models.CharField(max_length=200, blank=True)
    # WGS84 lat/lng polygons, matching the frontend map and GeoJSON output.
    geom = gis_models.PolygonField(srid=4326)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "lot geometry"
        verbose_name_plural = "lot geometries"
        ordering = ("listing_id",)

    def __str__(self):
        return f"Lot {self.listing_id}"
