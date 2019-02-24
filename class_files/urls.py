from django.urls import path
from . import views


app_name = 'class_files'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
]