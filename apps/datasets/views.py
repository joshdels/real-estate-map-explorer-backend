from django.http import Http404
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import AppDataset
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
        return Response(saved.payload)
