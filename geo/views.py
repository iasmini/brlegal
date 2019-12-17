from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from geo.models import State, CourtDistrict
from geo import serializers


class StateViewSet(viewsets.ModelViewSet):
    """Manage states in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = State.objects.all()
    serializer_class = serializers.StateSerializer

    def get_queryset(self):
        """Retrieve the states for the authenticated user"""
        queryset = self.queryset

        return queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Create a new state"""
        serializer.save(user=self.request.user)


class CourtDistrictViewSet(viewsets.ModelViewSet):
    """Manage court districts in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = CourtDistrict.objects.all()
    serializer_class = serializers.CourtDistrictSerializer

    def get_queryset(self):
        """Retrieve the court districts for the authenticated user"""

        # filtra as comarcas pelo estado, se informado
        state = self.request.query_params.get('state')
        queryset = self.queryset
        if state:
            state_id = [int(state)]
            queryset = queryset.filter(state__id__in=state_id)

        return queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Create a new court district"""
        serializer.save(user=self.request.user)
