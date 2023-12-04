from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth import get_user_model



# Modelo para Guardar de operarios (datos, usuario y fecha)

class Datos(models.Model):
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    usuario = models.CharField(max_length=150)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    campo1 = models.CharField(max_length=255)
    campo2 = models.IntegerField()

    def save(self, *args, **kwargs):
        
        super().save(*args, **kwargs)
        

    def __str__(self):
        return self.campo1

class licuefac(models.Model):
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    usuario = models.CharField(max_length=150)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    campo1 = models.CharField(max_length=255)
    campo2 = models.IntegerField()

    def save(self, *args, **kwargs):
        
        super().save(*args, **kwargs)
        

    def __str__(self):
        return self.campo1

class molienda(models.Model):
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    usuario = models.CharField(max_length=150)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    campo1 = models.CharField(max_length=255)
    campo2 = models.IntegerField()

    def save(self, *args, **kwargs):
        
        super().save(*args, **kwargs)
        

    def __str__(self):
        return self.campo1



 # Modelo CARGAR INCIDENTES (datos, usuario y fecha)

class Incidente(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)






class Task(models.Model):
  title = models.CharField(max_length=200)
  description = models.TextField(max_length=1000)
  created = models.DateTimeField(auto_now_add=True)
  datecompleted = models.DateTimeField(null=True, blank=True)
  important = models.BooleanField(default=False)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.title + ' - ' + self.user.username