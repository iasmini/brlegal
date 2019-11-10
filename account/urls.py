from django.urls import path

from account import views


app_name = 'account'

urlpatterns = [
    path('users/', views.ListCreateUserView.as_view(), name='users'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
]
