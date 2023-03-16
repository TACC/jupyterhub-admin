"""jupyterhub_admin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import include, path
import os

url_prefix = os.environ.get('URL_PREFIX', '').rstrip('/')
if url_prefix != '':
    url_prefix = url_prefix+'/'

urlpatterns = [
    path(f'{url_prefix}admin/', admin.site.urls),
    path(f'{url_prefix}jhub/', include('jupyterhub_admin.apps.jupyterhub.urls')),
    path(f'{url_prefix}images/', include('jupyterhub_admin.apps.images.urls')),
    path(f'{url_prefix}mounts/', include('jupyterhub_admin.apps.mounts.urls')),
    path(f'{url_prefix}groups/', include('jupyterhub_admin.apps.groups.urls')),
    path(f'{url_prefix}auth/', include('jupyterhub_admin.apps.tapisauth.urls')),
    path(f'{url_prefix}links/', include('jupyterhub_admin.apps.links.urls')),
    path(f'{url_prefix}logdata/', include('jupyterhub_admin.apps.logdata.urls')),
    path(f'{url_prefix}', include('jupyterhub_admin.apps.main.urls'))
]