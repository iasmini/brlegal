from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient, Recipe
from recipe import serializers


class BaseRecipeAttrViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    """Base viewset for usere owned recipe attributes"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        # 'assigned_only', 0: o zero significa que se o assigned_only for None
        # retorna zero (valor default para None)
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )
        queryset = self.queryset
        if assigned_only:
            # filtra somente receitas com tags ou ingredientes
            queryset = queryset.filter(recipe__isnull=False)

        return queryset.filter(
            user=self.request.user).order_by('-name').distinct()

    def perform_create(self, serializer):
        """Create a new base recipe attribute"""
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in the database"""
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSet(BaseRecipeAttrViewSet):
    """Manage ingredients in the database"""
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer

    # quando coloca o "_" antes do nome da funcao vc esta dizendo que eh uma
    # funcao que tem a intencao de ser privada (no python todas sao publicas)
    def _convert_params_to_ints(self, qs):
        """Convert a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        """Retrieve the recipes for the authenticated user"""

        # filtra as receitas pelas tags e ingredientes, se informados
        tags = self.request.query_params.get('tags')
        queryset = self.queryset
        if tags:
            tag_ids = self._convert_params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)

        ingredients = self.request.query_params.get('ingredients')
        if ingredients:
            ingredient_ids = self._convert_params_to_ints(ingredients)
            queryset = queryset.filter(ingredients__id__in=ingredient_ids)

        return queryset.filter(user=self.request.user)

    # this is the function that's called to retrieve the serializer class for
    # a particular request and it is this function that you would use if you
    # wanted to change the serializer class for the different actions that are
    # available
    # we have a number of actions available on by default in the model we use
    # One of them is a list in which case we just want to return the default
    # and that the other action is retrieve, in which case we want to return
    # the details of the serializer.
    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer
        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer

        return serializers.RecipeSerializer

    def perform_create(self, serializer):
        """Create a new recipe"""
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to an existing recipe"""
        # retrive the recipe object that is being accessed based on the id in
        # the url
        recipe = self.get_object()
        # aqui poderia ter sido usado direto o RecipeImageSerializer, mas a
        # boa pratica pede pra usar get_serializer e retornar nessa funcao
        # o serializer de acordo com o action. Dessa forma o django rest
        # sabe qual serializer deve mostrar no browser
        serializer = self.get_serializer(
            recipe,
            data=request.data
        )

        if serializer.is_valid():
            # save the recipe model with the updated data
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
