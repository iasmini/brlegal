from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from account.serializers import UserSerializer, AuthTokenSerializer
from django.contrib.auth import get_user_model


class CreateUserView(generics.CreateAPIView):
    """Create new user in the system"""
    serializer_class = UserSerializer


class ListUserView(generics.ListAPIView):
    """List the users in the system"""
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create new auth token for user"""
    serializer_class = AuthTokenSerializer
    # sets the renderer to view in the browser
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    # authentication is the mechanism by which the authentication happens
    # this could be cookie authentication or we're going to use token
    # authentication
    # it takes the authenticated user and assign it to request
    authentication_classes = (authentication.TokenAuthentication,)
    # permissions are the level of access that the user has. the only
    # permission we're going to add is that the user must be authenticated
    # to use the API
    permission_classes = (permissions.IsAuthenticated,)

    # what would happen with an API view is you would link it to a module to
    # retrieve the item and you would retrieve database models
    # In this case we're going to get the model for the log in user.
    # So we're going to override the get objects.
    # And we're just going to return the user that is authenticated.
    def get_object(self):
        """Retrieve and return authentication user"""
        return self.request.user
