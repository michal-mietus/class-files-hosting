import os
from datetime import datetime
from django.views.generic import DetailView, ListView, FormView, TemplateView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.http import Http404
from django.shortcuts import render
from .models import Section, File
from .forms import FileUploadForm, LoginForm, RegisterForm
from .api_token import TOKEN
import dropbox


class HomeView(ListView):
    model = Section
    template_name = 'class_files/home.html'
    context_object_name = 'sections'
    icon_path = 'static/icons/sections/'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        for section in context['sections']:
            section.icon_path = self.icon_path + section.icon_name
        return context


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'class_files/login.html'
    success_url = reverse_lazy('class_files:home')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        return render(self.request, self.template_name, {
            'form': form,
            'error': 'Username or password is wrong. Try again.',
        })




class SectionView(TemplateView):
    template_name = 'class_files/section.html'
    allowed_file_types = ['images', 'docs']  # TODO shared the same in SectionFilesView!
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['section'] = Section.objects.get(pk=self.kwargs['pk'])
        context['file_types'] = self.allowed_file_types
        return context


class SectionFilesView(DetailView):
    """
        Section in url have file type argument, on which depends which 
        files will be server.
    """
    model = Section
    context_object_name = 'section'
    template_name = 'class_files/section_files.html'
    allowed_file_types = ['images', 'docs']  # the same as in the SectionView

    def dispatch(self, request, *args, **kwargs):
        if kwargs['type'] not in self.allowed_file_types:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        section = Section.objects.get(pk=self.kwargs['pk'])
        context['files'] = section.get_files_typeof(self.kwargs['type'])
        dbx = self.dropbox_connection()
        context = self.get_link_or_delete_from_context(dbx, context)
        return context

    def get_dbx_link_or_delete_from_context(self, connection, context):
        """ If file from db cant be find in hosting, is deleting from context """
        for f in context['files']:
            try:
                f.link = self.get_file_link(dbx, f)
            except Exception as e:
                context['files'].filter(pk=f.pk).delete()
        return context

    def dropbox_connection(self):
        return dropbox.Dropbox(TOKEN)

    def get_file_link(self, dropbox_connection, file):
        return dropbox_connection.files_get_temporary_link(file.dropbox_path).link
        

class UploadFile(FormView):
    dropbox_folder_name = '/class-files/'
    form_class = FileUploadForm
    template_name = 'class_files/upload_file.html'
    success_url = reverse_lazy('class_files:home')

    def form_valid(self, form):
        dbx = self.dropbox_connection()
        files = self.request.FILES.getlist('file_field')
        for f in files:
            filename = self.create_file_name(f)
            file_path = self.create_dropbox_file_path(f)

            file_metadata = dbx.files_upload(f.file.read(), file_path)
            File.objects.create(
                name=filename,
                dropbox_path=file_path,
                extension=self.get_file_extension(f),
                section=self.get_section(),
                upload_date=datetime.now()
            )
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
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
