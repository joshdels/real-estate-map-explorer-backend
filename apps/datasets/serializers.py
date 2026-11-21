from rest_framework import serializers

from .models import AppDataset

REQUIRED_LISTING_FIELDS = {
    "id",
    "title",
    "address",
    "coordinates",
    "polygon",
    "area",
    "price",
    "status",
    "utilities",
}


class DatasetPayloadSerializer(serializers.Serializer):
    """OpenAPI representation of the temporary whole-dataset contract."""

    properties = serializers.ListField(child=serializers.DictField())
    providers = serializers.ListField(child=serializers.DictField())
    groups = serializers.ListField(child=serializers.DictField())
    reviews = serializers.ListField(child=serializers.DictField())
    metadata = serializers.DictField(required=False)
    utilities = serializers.DictField(required=False)
    agent = serializers.DictField(required=False)


def validate_dataset_payload(payload):
    if not isinstance(payload, dict):
        raise serializers.ValidationError("The dataset must be a JSON object.")
    for key in ("properties", "providers", "groups", "reviews"):
        if not isinstance(payload.get(key), list):
            raise serializers.ValidationError({key: "This field must be a list."})
    for index, listing in enumerate(payload["properties"]):
        if not isinstance(listing, dict) or not REQUIRED_LISTING_FIELDS.issubset(listing):
            raise serializers.ValidationError(
                {"properties": f"Listing {index} is missing required fields."}
            )
        if not isinstance(listing["coordinates"], list) or len(listing["coordinates"]) != 2:
            raise serializers.ValidationError(
                {"properties": f"Listing {index} has invalid coordinates."}
            )
        if not isinstance(listing["polygon"], list) or len(listing["polygon"]) < 3:
            raise serializers.ValidationError(
                {"properties": f"Listing {index} needs at least three boundary points."}
            )
    return payload


class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppDataset
        fields = ("payload",)

    def validate_payload(self, value):
        return validate_dataset_payload(value)
