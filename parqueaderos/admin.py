from django.contrib import admin

from parqueaderos.models import Usuario, Vehiculo, RegistroBitacora, Tarifa

# Register your models here.

admin.site.register(Usuario)
admin.site.register(Vehiculo)
admin.site.register(RegistroBitacora)
admin.site.register(Tarifa)
