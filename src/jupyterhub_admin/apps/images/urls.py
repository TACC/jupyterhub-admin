from django.urls import path
from . import views

app_name = 'images'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:index>', views.images, name='images'),
    path('new/', views.new_image, name='new'),
    path('api/', views.api, name='api')
]