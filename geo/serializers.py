from rest_framework import serializers

from geo.models import CourtDistrict, State


class StateSerializer(serializers.ModelSerializer):
    """Serializer for state objects"""

    class Meta:
        model = State
        fields = ('id', 'name', 'initials')
        read_only_fields = ('id',)


class CourtDistrictSerializer(serializers.ModelSerializer):
    """Serialize a court district"""
    state = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=State.objects.all()
    )

    class Meta:
        model = CourtDistrict
        fields = ('id', 'name', 'state')
        read_only_fields = ('id',)


class CourtDistrictDetailSerializer(CourtDistrictSerializer):
    """Serialize a court district detail"""
    state = StateSerializer(many=False, read_only=True)
