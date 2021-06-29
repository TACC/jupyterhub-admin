from django.urls import path
from . import views

app_name = 'groups'
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:group>', views.groups, name='groups'),
    path('create/', views.create_group, name='create_group'),
    path('rename/', views.rename_group, name='rename_group'),
    path('delete/', views.delete_group, name='delete_group'),
    path('api/<str:group>', views.api, name='api')
]