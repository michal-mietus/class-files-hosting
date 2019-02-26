from django.urls import path
from . import views


app_name = 'class_files'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('section/<int:pk>', views.SectionView.as_view(), name='section'),
    path('section/<int:pk>/<str:type>', views.SectionFilesView.as_view(), name='section_files'),
    # dont know why this pattern doesnt work
    #path('section/<int:pk>/upload', views.UploadFile.as_view(), name='upload_file')
    path('section/upload/<int:pk>', views.UploadFile.as_view(), name='upload_file')
]