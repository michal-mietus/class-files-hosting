from django.views.generic import ListView
from .models import Section


class Home(ListView):
    template_name = 'class_files/home.html'
    model = Section
    context_object_name = 'sections'
