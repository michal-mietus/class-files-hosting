from django.views.generic import DetailView, ListView
from .models import Section, File


class SectionView(DetailView):
    model = Section
    context_object_name = 'section'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        section = Section.objects.get(pk=self.kwargs['pk'])
        context['files'] = section.get_all_files()
        return context


class HomeView(ListView):
    model = Section
    template_name = 'class_files/home.html'
    context_object_name = 'sections'
