from django.urls import path
from . import views

app_name = 'groups'
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:group>', views.groups, name='groups'),
    path('create/', views.create_group, name='create_group'),
    path('rename/', views.rename_group, name='rename_group'),
    path('delete/', views.delete_group, name='delete_group'),
    path('<str:group>/user/<str:index>', views.user, name='user'),
    path('api/<str:group>/user/<str:index>', views.user_api, name='user_api')
]