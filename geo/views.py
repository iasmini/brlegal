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
        # # 'assigned_only', 0: o zero significa que se o assigned_only for None
        # # retorna zero (valor default para None)
        # assigned_only = bool(
        #     int(self.request.query_params.get('assigned_only', 0))
        # )
        # queryset = self.queryset
        # if assigned_only:
        #     # filtra somente receitas com tags ou ingredientes
        #     queryset = queryset.filter(recipe__isnull=False)
        #
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

    # this is the function that's called to retrieve the serializer class for
    # a particular request and it is this function that you would use if you
    # want to change the serializer class for the different actions that are
    # available
    # we have a number of actions available by default in the model. we used 2.
    # one of them is a list in which case we just want to return the default
    # and that the other action is retrieve, in which case we want to return
    # the details of the serializer.
    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.CourtDistrictDetailSerializer

        return serializers.CourtDistrictSerializer

    def perform_create(self, serializer):
        """Create a new court district"""
        serializer.save(user=self.request.user)
