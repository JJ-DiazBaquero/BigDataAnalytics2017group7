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
