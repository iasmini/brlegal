from django.urls import path

from account import views


app_name = 'account'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('list/', views.ListUserView.as_view(), name='list'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
]
