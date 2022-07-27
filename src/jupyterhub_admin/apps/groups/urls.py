from django.urls import path
from . import views

app_name = 'groups'
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:group>', views.groups, name='groups'),
    path('create/', views.create_group, name='create_group'),
    path('rename/', views.rename_group, name='rename_group'),
    path('delete/', views.delete_group, name='delete_group'),
    path('stop/', views.stop_all_servers, name='stop_all_servers'),
    path('<str:group>/user/<str:index>', views.user, name='user'),
    path('<str:group>/images/<str:index>', views.images, name='images'),
    path('<str:group>/mounts/<str:index>', views.mounts, name='mounts'),
    path('api/<str:group>/user/<str:index>', views.user_api, name='user_api'),
    path('api/<str:group>/images/<str:index>', views.images_api, name='images_api'),
    path('api/<str:group>/mounts/<str:index>', views.mounts_api, name='mounts_api')
]