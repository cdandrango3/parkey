from django.db import models

# Create your models here.


class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.EmailField()
    telefono = models.CharField(max_length=15)
    es_oficinista = models.BooleanField(default=False)
    num_oficina = models.CharField(max_length=5)
    saldo = models.FloatField()


class Vehiculo(models.Model):
    placa = models.CharField(max_length=15, unique=True)
    color = models.CharField(max_length=50)
    vehiculo_usuario = models.ManyToManyField(Usuario)


class RegistroBitacora(models.Model):
    hora_entrada = models.DateTimeField()
    hora_salida = models.DateTimeField()
    imagen_vehiculo_entrada = models.ImageField(upload_to='capturas/')
    imagen_vehiculo_salida = models.ImageField(upload_to='capturas/')
    precio_total = models.FloatField()
    id_vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)


class Tarifa(models.Model):
    horas = models.IntegerField()
    precio = models.FloatField()