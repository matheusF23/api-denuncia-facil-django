from rest_framework import serializers

from drf_extra_fields.fields import Base64ImageField

from ..models import Occurrence


class OccurrenceSerializer(serializers.ModelSerializer):
    """Serializer a Occurrence"""
    image = Base64ImageField()

    class Meta:
        model = Occurrence
        fields = ['id', 'license_plate', 'occurrence_type', 'occurrence_title',
                  'location', 'observation', 'anonymous', 'image', 'created_at']
        read_only_fields = ('id',)

    def create(self, validated_data):
        image = validated_data.pop('image')
        return Occurrence.objects.create(image=image, **validated_data)
