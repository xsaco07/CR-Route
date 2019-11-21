from django.db import models

class Empresa(models.Model):
    nombre = models.CharField(max_length=30)
    zona = models.CharField(max_length=50)
    telefono = models.CharField(max_length=30)
    correo = models.EmailField()
    direccion = models.CharField(max_length=30)
    latitud = models.FloatField()
    longitud = models.FloatField()
    horario = models.TextField()

class Ruta(models.Model):
    numero_ruta = models.IntegerField()
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=200)
    precio = models.IntegerField()
    horario = models.TextField()
    duracion = models.IntegerField()
    rampa = models.BooleanField()

class Punto(models.Model):
    ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE)
    serial = models.IntegerField()
    latitud = models.FloatField()
    longitud = models.FloatField()
    esParada = models.BooleanField()
    descripcion = models.CharField(max_length=100)

class Usuario(models.Model):
    nombre_usuario = models.CharField(max_length=30)
    nombre = models.CharField(max_length=30)
    apellido1 = models.CharField(max_length=30)
    apellido2 = models.CharField(max_length=30)
    contrasena = models.CharField(max_length=30)

class Log(models.Model):
    nombre_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    accion = models.CharField(max_length=30)
    tabla = models.CharField(max_length=30)
    hora = models.DateTimeField(auto_now_add=True) # don't need to pass this value to constructor
