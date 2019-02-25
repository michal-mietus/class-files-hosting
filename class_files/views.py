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


class UploadFile(FormView):
    dropbox_folder_name = '/class-files/'
    form_class = FileUploadForm
    template_name = 'class_files/upload_file.html'
    success_url = reverse_lazy('class_files:home')


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['pk'] = self.kwargs['pk']
        return context

    def dropbox_connection(self):
        return dropbox.Dropbox(TOKEN)

    def create_file_name(self, file):
        """
            Filename pattern: 
                basename + '_' + date(spaces replaced with underscores) + file_extension
        """
        basename, extension = os.path.splitext(str(file))
        filename = basename + '_' + self.get_formatted_date() + extension
        return filename

    def get_file_extension(self, file):
        basename, extension = os.path.splitext(str(file))
        return extension

    def get_formatted_date(self):
        return str(datetime.now()).replace(' ', '_')

    def create_dropbox_file_path(self, file_name):
        return self.get_dropbox_section_folder_path() + str(file_name)

    def get_dropbox_section_folder_path(self):
        return self.dropbox_folder_name + str(self.get_section()).lower() + '/' 

    def get_section(self):
        return Section.objects.get(pk=self.kwargs['pk'])
