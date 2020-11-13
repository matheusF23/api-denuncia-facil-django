from rest_framework import serializers

from ..models import Occurrence


class OccurrenceSerializer(serializers.ModelSerializer):
    """Serializer a Occurrence"""

    class Meta:
        model = Occurrence
        fields = ['id', 'license_plate', 'occurrence_type', 'occurrence_title',
                  'location', 'observation', 'anonymous', 'created_at']
        read_only_fields = ('id',)
