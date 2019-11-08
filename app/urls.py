"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT): what this does
# is it makes the media url available in a development server so we can test
# uploading images for our recipes without having to set up a separate web
# server for serving these media files.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('account.urls')),
]
