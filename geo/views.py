from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from geo.models import State, CourtDistrict
from geo import serializers


class BaseCourtDistrictAttrViewSet(viewsets.GenericViewSet,
                                   mixins.ListModelMixin,
                                   mixins.CreateModelMixin):
    """Base viewset for user owned court district attributes"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""

        print(self.request.user)
        print(self.request.auth)

        return self.queryset.filter(
            user=self.request.user).order_by('-name').distinct()

    def perform_create(self, serializer):
        """Create a new base court district attribute"""
        serializer.save(user=self.request.user)


class StateViewSet(BaseCourtDistrictAttrViewSet):
    """Manage states in the database"""
    queryset = State.objects.all()
    serializer_class = serializers.StateSerializer


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
            state_id = int(state)
            queryset = queryset.filter(state__id__in=state_id)

        return queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        return serializers.CourtDistrictSerializer

    def perform_create(self, serializer):
        """Create a new court district"""
        serializer.save(user=self.request.user)
