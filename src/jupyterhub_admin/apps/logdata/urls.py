from django.urls import path
from . import views

app_name="logdata"
urlpatterns = [
    path('', views.index, name='index'),
]