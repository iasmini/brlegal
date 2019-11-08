from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipe import views

# default router is a feature of the Django rest framework that automatically
# generate the urls for our viewset
# what the default router does is it automatically registers the appropriate
# urls for all of the actions in our view set
router = DefaultRouter()
router.register('tags', views.TagViewSet)
router.register('ingredients', views.IngredientViewSet)
router.register('recipes', views.RecipeViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls)),
]
