from datetime import datetime

from django.shortcuts import render, redirect
import logging
# Create your views here.
from parqueaderos.models import Vehiculo, RegistroBitacora,Usuario

DICT = {
        "nombreEmpresa" : "Plaza del Rancho",
        "modulos": ["Bitácora", "Oficinistas", "Reportes"] # Posibilidad de traer desde la base
    }

def index(request):
    global DICT
    return render(request, "Base.html", DICT)
def createof(request):
    global DICT
    placa = request.GET.get('placa')
    oficina = request.GET.get('oficina')
    oficinista = request.GET.get('oficinista')
    placa=Vehiculo(placa=placa,color="red")
    person=Usuario(nombre=oficinista,es_oficinista=True,num_oficina=oficina,saldo=0)
    placa.save()
    person.save()
    placa.vehiculo_usuario.add(person.id)



    return redirect("/oficinistas/")

def bitacora(request):
    global DICT
    """Datos extraidos del servidor por medio de una consulta:
    [placa, fecha, hora_entrada, hora_salida, estado]
    estado es calculado"""
    c = RegistroBitacora.objects.all()

    datos = []
    for placa in c:
        dic2 = {}
        pla = Vehiculo.objects.get(id=placa.id_vehiculo_id)
        dic2["placa"] = pla.placa
        d = placa.hora_entrada
        h_s=placa.hora_salida
        spl = d.strftime("%m/%d/%Y, %H:%M:%S").split()

        dic2["fecha"] = spl[0]
        dic2["hora"] = spl[1]
        if h_s is None:
            dic2["salida"] = "-"
            dic2["final"] = "en espera"
        else:
            spl2 = h_s.strftime("%m/%d/%Y, %H:%M:%S").split()
            dic2["salida"] = spl2[1]
            time_1 = datetime.strptime(spl[1], "%H:%M:%S")
            time_2 = datetime.strptime(spl2[1], "%H:%M:%S")
            timef=time_2-time_1
            tiempomax=6
            hf = str(timef).split(":")[0]
            """check if is a employee"""
            of=pla.vehiculo_usuario.through.objects.get(vehiculo_id=placa.id_vehiculo_id);
            isof=Usuario.objects.get(id=of.usuario_id)
            if isof.es_oficinista:
                dic2["final"] = "permitido"
            if(tiempomax>int(hf)):
                dic2["final"] = "permitido"
            else:
                if(tiempomax <int(hf)):
                    dic2["final"] = "excedido"

        datos.append(dic2)
    DICT["datosServidor"] = datos
    return render(request, "Bitacora.html",DICT)

def oficinistas(request):
    global DICT
    """Datos extraidos del servidor por medio de una consulta:
    [placa, num_oficina, nombre + apellido]"""
    logging.debug("Log message goes here.")
    datos=[]
    pop=Vehiculo.objects.all();
    DICT["placas"] = pop
    c=Vehiculo.vehiculo_usuario.through.objects.all()
    for ad in c:
        dic2 = {}
        pla = Vehiculo.objects.get(id=ad.vehiculo_id)
        us = Usuario.objects.get(id=ad.usuario_id)
        dic2["placa"] = pla.placa
        dic2["oficinista"] = us.nombre
        dic2["oficina"] = us.num_oficina
        datos.append(dic2)
    DICT["datosServidor"] =datos
    return render(request, "Oficinistas.html", DICT)

def reportes(request):
    return render(request, "Base.html", DICT)

