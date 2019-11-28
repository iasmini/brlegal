from rest_framework import serializers

from geo.models import CourtDistrict, State


class StateSerializer(serializers.ModelSerializer):
    """Serializer for state objects"""

    class Meta:
        model = State
        fields = ('id', 'name', 'initials', 'court_districts')
        read_only_fields = ('id',)


class CourtDistrictSerializer(serializers.ModelSerializer):
    """Serialize a court district"""

    state = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=State.objects.all()
    )

    class Meta:
        model = CourtDistrict
        fields = ('id', 'name', 'state')
        read_only_fields = ('id',)
