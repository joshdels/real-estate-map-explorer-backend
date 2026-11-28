"""Sync the dataset blob's listing polygons into normalized PostGIS geometry.

Frontend and dataset coordinates are ``[latitude, longitude]`` pairs. PostGIS /
GeoJSON use ``(longitude, latitude)`` with SRID 4326, so conversion happens
here, at the boundary, and nowhere else.
"""

from __future__ import annotations

from django.contrib.gis.geos import GEOSException, Polygon

from .models import LotGeometry


def polygon_from_points(points) -> Polygon | None:
    """Build a closed WGS84 ``Polygon`` from ``[[lat, lng], ...]`` points."""
    if not isinstance(points, list) or len(points) < 3:
        return None
    ring: list[tuple[float, float]] = []
    for point in points:
        if not isinstance(point, (list, tuple)) or len(point) != 2:
            return None
        try:
            lat = float(point[0])
            lng = float(point[1])
        except (TypeError, ValueError):
            return None
        # GeoJSON/PostGIS order is (lng, lat).
        ring.append((lng, lat))
    if ring[0] != ring[-1]:
        ring.append(ring[0])
    if len(ring) < 4:
        return None
    try:
        return Polygon(ring, srid=4326)
    except (GEOSException, ValueError, TypeError):
        return None


def sync_lot_geometries(payload) -> dict[str, int]:
    """Upsert one ``LotGeometry`` per listing and drop geometries that are gone.

    Returns a small summary so callers can log how many rows changed. A listing
    with an unusable polygon is skipped (and its stale geometry removed) rather
    than aborting the whole save; the blob remains the source of truth.
    """
    properties = payload.get("properties") if isinstance(payload, dict) else None
    if not isinstance(properties, list):
        properties = []

    seen: set[str] = set()
    written = 0
    for listing in properties:
        if not isinstance(listing, dict):
            continue
        listing_id = listing.get("id")
        if not isinstance(listing_id, str) or not listing_id:
            continue
        polygon = polygon_from_points(listing.get("polygon"))
        if polygon is None:
            continue
        title = listing.get("title")
        LotGeometry.objects.update_or_create(
            listing_id=listing_id,
            defaults={
                "geom": polygon,
                "title": title if isinstance(title, str) else "",
            },
        )
        seen.add(listing_id)
        written += 1

    removed, _ = LotGeometry.objects.exclude(listing_id__in=seen).delete()
    return {"written": written, "removed": removed}
