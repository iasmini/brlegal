from django.urls import path, include
from rest_framework.routers import DefaultRouter

from geo import views

# default router is a feature of the Django rest framework that automatically
# generate the urls for our viewset
# what the default router does is it automatically registers the appropriate
# urls for all of the actions in our view set
router = DefaultRouter()
router.register('states', views.StateViewSet)
router.register('court-districts', views.CourtDistrictViewSet)

app_name = 'geo'

urlpatterns = [
    path('', include(router.urls)),
]
