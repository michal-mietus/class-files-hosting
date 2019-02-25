from django.urls import path
from . import views


app_name = 'class_files'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('section/<int:pk>', views.SectionView.as_view(), name='section'),
    path('section/<int:pk>/upload', views.UploadFile.as_view(), name='upload_file')
]