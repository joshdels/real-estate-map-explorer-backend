import json

from django.core.serializers import serialize
from django.http import Http404, HttpResponse
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .geometry import sync_lot_geometries
from .models import AppDataset, LotGeometry
from .permissions import CanReplaceDataset
from .serializers import (
    DatasetPayloadSerializer,
    DatasetSerializer,
    validate_client_replacement,
)


class DatasetView(APIView):
    def get_permissions(self):
        return [AllowAny()] if self.request.method == "GET" else [CanReplaceDataset()]

    def get_object(self):
        dataset = AppDataset.objects.order_by("pk").first()
        if dataset is None:
            raise Http404("The dataset has not been seeded yet.")
        return dataset

    @extend_schema(
        operation_id="dataset_retrieve",
        summary="Get the shared dataset",
        description="Publicly returns the current validated whole-dataset JSON document.",
        responses={200: DatasetPayloadSerializer},
        auth=[],
        tags=["dataset"],
    )
    def get(self, request):
        return Response(self.get_object().payload)

    @extend_schema(
        operation_id="dataset_replace",
        summary="Replace the shared dataset",
        description=(
            "Replaces the temporary dataset blob. Staff may replace it; clients may change only "
            "records owned by their assigned provider."
        ),
        request=DatasetPayloadSerializer,
        responses={200: DatasetPayloadSerializer},
        tags=["dataset"],
    )
    def put(self, request):
        dataset = self.get_object()
        serializer = DatasetSerializer(dataset, data={"payload": request.data})
        serializer.is_valid(raise_exception=True)
        if request.user.role == "client":
            validate_client_replacement(
                dataset.payload,
                serializer.validated_data["payload"],
                request.user.provider_id,
            )
        saved = serializer.save()
        # Mirror every listing boundary into PostGIS so saved/edited plot points
        # persist as real geometry, not only inside the JSON blob.
        sync_lot_geometries(saved.payload)
        return Response(saved.payload)


class LotGeometryGeoJSONView(APIView):
    """Publicly serves every stored lot boundary as a GeoJSON FeatureCollection."""

    permission_classes = [AllowAny]

    @extend_schema(
        operation_id="lot_geometries_geojson",
        summary="Get lot boundaries as GeoJSON",
        description="Returns all stored listing boundaries from PostGIS as GeoJSON features.",
        responses={200: {"type": "object"}},
        auth=[],
        tags=["dataset"],
    )
    def get(self, request):
        collection = serialize(
            "geojson",
            LotGeometry.objects.all(),
            geometry_field="geom",
            fields=("listing_id", "title"),
        )
        return HttpResponse(
            json.dumps(json.loads(collection)),
            content_type="application/geo+json",
        )
