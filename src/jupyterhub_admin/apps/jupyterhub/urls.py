from django.urls import path
from . import views

app_name = 'jupyterhub'
urlpatterns = [
    path('', views.index, name='index'),
    path('users/<str:username>', views.user, name='user'),
    path('users/<str:username>/server', views.server, name='server')
]