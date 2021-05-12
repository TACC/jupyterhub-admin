from django.urls import path
from . import views

app_name = 'mounts'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:index>', views.mounts, name='mounts'),
    path('new/', views.new_mount, name='new'),
    path('api/<str:index>', views.api, name='api')
]