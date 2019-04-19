from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = 'class_files'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('section/<int:pk>', views.SectionView.as_view(), name='section'),
    path('section/<int:pk>/<str:type>', views.SectionFilesView.as_view(), name='section_files'),
    path('section/<int:pk>/upload/', views.UploadFile.as_view(), name='upload_file'),
]