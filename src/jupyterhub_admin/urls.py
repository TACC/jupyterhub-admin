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


urlpatterns = [
    path('admin/', admin.site.urls),
    path('jhub/', include('jupyterhub_admin.apps.jupyterhub.urls')),
    path('images/', include('jupyterhub_admin.apps.images.urls')),
    path('mounts/', include('jupyterhub_admin.apps.mounts.urls')),
    path('groups/', include('jupyterhub_admin.apps.groups.urls')),
    path('auth/', include('jupyterhub_admin.apps.tapisauth.urls')),
    path('links/', include('jupyterhub_admin.apps.links.urls')),
    path('', include('jupyterhub_admin.apps.main.urls'))
]
