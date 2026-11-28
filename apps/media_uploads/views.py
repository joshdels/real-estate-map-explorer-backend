from pathlib import Path
from uuid import uuid4

from django.core.files.storage import default_storage
from drf_spectacular.utils import extend_schema
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import PropertyImageUploadSerializer


class PropertyImageUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(
        operation_id="property_image_upload",
        summary="Upload a property image",
        request=PropertyImageUploadSerializer,
        responses={201: {"type": "object", "properties": {"url": {"type": "string"}}}},
        tags=["media"],
    )
    def post(self, request):
        serializer = PropertyImageUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        image = serializer.validated_data["image"]
        suffix = Path(image.name).suffix.lower() or ".jpg"
        name = default_storage.save(f"property-media/{uuid4().hex}{suffix}", image)
        return Response({"url": request.build_absolute_uri(default_storage.url(name))}, status=201)
