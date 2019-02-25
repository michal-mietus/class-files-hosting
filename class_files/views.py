import os
from datetime import datetime
from django.views.generic import DetailView, ListView, FormView
from django.urls import reverse_lazy
from .models import Section, File
from .forms import FileUploadForm
from .api_token import TOKEN
import dropbox


class HomeView(ListView):
    model = Section
    template_name = 'class_files/home.html'
    context_object_name = 'sections'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        for section in context['sections']:
            section.icon_path = 'static/icons/' + section.icon_name
        return context


class SectionView(DetailView):
    model = Section
    context_object_name = 'section'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        section = Section.objects.get(pk=self.kwargs['pk'])
        context['files'] = section.get_all_files()
        return context

