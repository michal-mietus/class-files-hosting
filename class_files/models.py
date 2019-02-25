from django.db import models


class Section(models.Model):
    name = models.CharField(max_length=30)
    icon_name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    def get_all_files(self):
        return self.file_set.all()


class File(models.Model):
    name = models.CharField(max_length=100)
    dropbox_path = models.URLField()
    extension = models.CharField(max_length=100)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    creation_date = models.DateField()
