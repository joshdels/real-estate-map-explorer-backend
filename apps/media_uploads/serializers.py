from rest_framework import serializers

MAX_IMAGE_BYTES = 10 * 1024 * 1024


class PropertyImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()

    def validate_image(self, image):
        if image.size > MAX_IMAGE_BYTES:
            raise serializers.ValidationError("Images must be 10 MB or smaller.")
        if image.content_type not in {"image/jpeg", "image/png", "image/webp"}:
            raise serializers.ValidationError("Upload a JPEG, PNG, or WebP image.")
        return image
