from django.db import models


class Section(models.Model):
    name = models.CharField(max_length=30)


class File(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()
    extension = models.CharField(max_length=100)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
