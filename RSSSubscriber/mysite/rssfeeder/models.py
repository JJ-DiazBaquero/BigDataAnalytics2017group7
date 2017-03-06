from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
import datetime
from django.db import models

# Create your models here.
class Profesor(models.Model):
    nombre = models.CharField(max_length=100, primary_key = True)
    departamento = models.CharField(max_length=100,blank=True, null= True)
    cargo = models.CharField(max_length=100,blank=True, null= True)
    curso= models.CharField(max_length=100,blank=True, null= True)
    correo = models.CharField(max_length=100,blank=True, null= True)
    estudios = models.CharField(max_length=100,blank=True, null= True)
    extension = models.CharField(max_length=100,blank=True, null= True)
    sitioWeb = models.CharField(max_length=100,blank=True, null= True)
    oficina = models.CharField(max_length=100,blank=True, null= True)
    area = models.CharField(max_length=100,blank=True, null= True)
    grupoInvestigacion = models.CharField(max_length=100,blank=True, null= True)

@python_2_unicode_compatible
class Post(models.Model):
    post_title = models.CharField(max_length=200)
    post_description = models.TextField()
    post_published_date = models.DateTimeField('date published')
    post_link = models.CharField(max_length=400)

    def __str__(self):
        return self.post_title