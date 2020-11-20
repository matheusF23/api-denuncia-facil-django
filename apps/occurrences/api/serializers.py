from rest_framework import serializers

from drf_extra_fields.fields import Base64ImageField

from ..models import Occurrence


class OccurrenceSerializer(serializers.ModelSerializer):
    """Serializer a Occurrence"""
    image = Base64ImageField(required=False)

    class Meta:
        model = Occurrence
        fields = ['id', 'license_plate', 'occurrence_type', 'occurrence_title',
                  'location', 'observation', 'anonymous', 'status', 'created_at', 'image']
        read_only_fields = ('id', 'status')

    def create(self, validated_data):
        image = validated_data.pop('image', None)
        return Occurrence.objects.create(image=image, **validated_data)
