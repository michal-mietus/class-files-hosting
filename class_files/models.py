from django.db import models


class Section(models.Model):
    name = models.CharField(max_length=30)
    icon_name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    def get_all_files(self):
        return self.file_set.all()

    def get_files_typeof(self, file_type):
        # TODO I dont know is this place good for that logic
        if file_type == 'images':
            extensions = ['.jpeg', '.jpg', '.png', '.gif']
        elif file_type == 'docs':
            extensions = ['.pdf', '.csv']
        else:
            extensions = []

        return self.file_set.filter(extension__in=extensions)


class File(models.Model):
    name = models.CharField(max_length=100)
    dropbox_path = models.URLField()
    extension = models.CharField(max_length=100)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    upload_date = models.DateField()

    def __str__(self):
        return self.name
