from django.urls import path, include
from rest_framework.routers import DefaultRouter

from geo import views

# default router is a feature of the Django rest framework that automatically
# generate the urls for our viewset
# what the default router does is it automatically registers the appropriate
# urls for all of the actions in our view set

# https://www.django-rest-framework.org/api-guide/routers/
# Optionally, you may also specify an additional argument:
#
# basename - The base to use for the URL names that are created.
# If unset the basename will be automatically generated based on the
# queryset attribute of the viewset, if it has one. Note that if the viewset
# does not include a queryset attribute then you must set basename when registering the viewset.
# The example above would generate the following URL patterns:
#
# URL pattern: ^users/$ Name: 'user-list'
# URL pattern: ^users/{pk}/$ Name: 'user-detail'
# URL pattern: ^accounts/$ Name: 'account-list'
# URL pattern: ^accounts/{pk}/$ Name: 'account-detail'
router = DefaultRouter()
router.register('states', views.StateViewSet)
router.register('court-districts', views.CourtDistrictViewSet)

app_name = 'geo'

urlpatterns = [
    path('', include(router.urls)),
]
