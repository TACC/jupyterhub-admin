from django.urls import path
from . import views

app_name = 'images'
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:admin>', views.images, name='admin'),
    path('new/', views.new_image, name='addadmin'),
    path('api/<str:admin>', views.api, name='api')
]