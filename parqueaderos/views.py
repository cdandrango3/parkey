import json
from datetime import datetime
from django.db.models import Count
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
import logging
# Create your views here.
from parqueaderos.models import Vehiculo, RegistroBitacora, Usuario

DICT = {
    "nombreEmpresa": "Plaza del Rancho",
    "modulos": ["Bitácora", "Oficinistas", "Reportes"]  # Posibilidad de traer desde la base
}


def index(request):
    global DICT
    return render(request, "Base.html", DICT)


def senddatag(request):
    getr = RegistroBitacora.objects.values('id_vehiculo_id') \
        .annotate(count=Count('id_vehiculo_id'))
    d = []
    for getgra in getr:
        dic1 = {}
        placa = Vehiculo.objects.get(id=getgra["id_vehiculo_id"])
        dic1["placa"] = placa.placa
        dic1["count"] = getgra["count"]
        d.append(dic1)
    dates = json.dumps(d)
    return HttpResponse(dates)


def createof(request):
    global DICT
    placa = request.GET.get('placa')
    oficina = request.GET.get('oficina')
    oficinista = request.GET.get('oficinista')
    fr = Vehiculo.objects.filter(placa=placa).exists()
    if fr != True:
        placa = Vehiculo(placa=placa, color="red")
        placa.save()
        person = Usuario(nombre=oficinista, es_oficinista=True, num_oficina=oficina, saldo=0)
        person.save()
        placa.vehiculo_usuario.add(person.id)
    else:
        placa = Vehiculo.objects.get(placa=placa)
        person = Usuario(nombre=oficinista, es_oficinista=True, num_oficina=oficina, saldo=0)
        person.save()
        placa.vehiculo_usuario.add(person.id)

    return redirect("/oficinistas/")

def notification(request):
    global DICT
    """Datos extraidos del servidor por medio de una consulta:
    [placa, fecha, hora_entrada, hora_salida, estado]
    estado es calculado"""
    c = RegistroBitacora.objects.all().order_by("hora_entrada")

    datos = []
    sumdic = {}
    temp_date = datetime.now()
    for placa in c:
        dic2 = {}
        pla = Vehiculo.objects.get(id=placa.id_vehiculo_id)
        dic2["placa"] = pla.placa
        d = placa.hora_entrada
        h_s = placa.hora_salida
        spl = d.strftime("%m/%d/%Y, %H:%M:%S").split()
        dic2["fecha"] = spl[0]
        dic2["hora"] = spl[1]
        tempc = temp_date.strftime("%m/%d/%Y, %H:%M:%S").split()[0]
        if tempc != spl[0]:
            sumdic = {}
        if h_s is None:
            dic2["salida"] = "-"
            dic2["final"] = "en espera"
        else:
            spl2 = h_s.strftime("%m/%d/%Y, %H:%M:%S").split()
            dic2["salida"] = spl2[1]
            time_1 = datetime.strptime(spl[1], "%H:%M:%S")
            time_2 = datetime.strptime(spl2[1], "%H:%M:%S")
            timef = time_2 - time_1
            tiempomax = 3
            hf = str(timef).split(":")[0]
            if is_key(sumdic, pla.placa):
                sumdic[pla.placa] = int(hf)
            else:
                hft = sumdic[pla.placa]
                hf = int(hf) + hft
                sumdic[pla.placa] = int(hf)

            """check if is a employee"""
            if Vehiculo.vehiculo_usuario.through.objects.filter(vehiculo_id=placa.id_vehiculo_id).exists():
                of = pla.vehiculo_usuario.through.objects.get(vehiculo_id=placa.id_vehiculo_id)
                isof = Usuario.objects.get(id=of.usuario_id)
                if isof.es_oficinista:
                    dic2["final"] = "permitido"
                else:
                    if (tiempomax > int(hf)):
                        dic2["final"] = "permitido"
                    else:
                        if (tiempomax < int(hf)):
                            dic2["final"] = "excedido"
            else:
                if (tiempomax >= int(hf)):
                    dic2["final"] = "permitido"
                else:
                    if (tiempomax < int(hf)):
                        dic2["final"] = "excedido"
        temp_date = placa.hora_entrada
        datos.append(dic2)
    datosj = json.dumps(datos)
    return HttpResponse(datosj)
def bitacora(request):
    global DICT
    """Datos extraidos del servidor por medio de una consulta:
    [placa, fecha, hora_entrada, hora_salida, estado]
    estado es calculado"""
    c = RegistroBitacora.objects.all().order_by("hora_entrada")

    datos = []
    sumdic = {}
    temp_date=datetime.now()
    for placa in c:
        dic2 = {}
        pla = Vehiculo.objects.get(id=placa.id_vehiculo_id)
        dic2["placa"] = pla.placa
        d = placa.hora_entrada
        h_s = placa.hora_salida
        spl = d.strftime("%m/%d/%Y, %H:%M:%S").split()
        dic2["fecha"] = spl[0]
        dic2["hora"] = spl[1]
        tempc=temp_date.strftime("%m/%d/%Y, %H:%M:%S").split()[0]
        if tempc != spl[0]:
            sumdic = {}
        if h_s is None:
            dic2["salida"] = "-"
            dic2["final"] = "en espera"
        else:
            spl2 = h_s.strftime("%m/%d/%Y, %H:%M:%S").split()
            dic2["salida"] = spl2[1]
            time_1 = datetime.strptime(spl[1], "%H:%M:%S")
            time_2 = datetime.strptime(spl2[1], "%H:%M:%S")
            timef = time_2 - time_1
            tiempomax = 3
            hf = str(timef).split(":")[0]
            if is_key(sumdic, pla.placa):
                sumdic[pla.placa] = int(hf)
            else:
                hft = sumdic[pla.placa]
                hf = int(hf)+hft
                sumdic[pla.placa] = int(hf)

            """check if is a employee"""
            if Vehiculo.vehiculo_usuario.through.objects.filter(vehiculo_id=placa.id_vehiculo_id).exists():
                of = pla.vehiculo_usuario.through.objects.get(vehiculo_id=placa.id_vehiculo_id)
                isof = Usuario.objects.get(id=of.usuario_id)
                if isof.es_oficinista:
                    dic2["final"] = "permitido"
                else:
                    if (tiempomax > int(hf)):
                        dic2["final"] = "permitido"
                    else:
                        if (tiempomax < int(hf)):
                            dic2["final"] = "excedido"
            else:
                if (tiempomax >= int(hf)):
                    dic2["final"] = "permitido"
                else:
                    if (tiempomax < int(hf)):
                        dic2["final"] = "excedido"
        temp_date=placa.hora_entrada
        datos.append(dic2)
    DICT["datosServidor"] = datos

    if is_ajax(request=request):
        placa = request.GET.get('placa')
        fechai = request.GET.get('fechai')
        fechaf = request.GET.get('fechaf')
        if not placa:
            c = RegistroBitacora.objects.filter(hora_entrada__range=(fechai, fechaf)).order_by("hora_entrada")
        if not fechai or not fechaf:
            c = RegistroBitacora.objects.filter(id_vehiculo_id__placa__contains=placa).order_by("hora_entrada")

        datos = []
        sumdic = {}
        for placa in c:
            dic2 = {}
            pla = Vehiculo.objects.get(id=placa.id_vehiculo_id)
            dic2["placa"] = pla.placa
            d = placa.hora_entrada
            h_s = placa.hora_salida
            spl = d.strftime("%m/%d/%Y, %H:%M:%S").split()
            dic2["fecha"] = spl[0]
            dic2["hora"] = spl[1]
            tempc = temp_date.strftime("%m/%d/%Y, %H:%M:%S").split()[0]
            if tempc != spl[0]:
                sumdic = {}
            if h_s is None:
                dic2["salida"] = "-"
                dic2["final"] = "en espera"
            else:
                spl2 = h_s.strftime("%m/%d/%Y, %H:%M:%S").split()
                dic2["salida"] = spl2[1]
                time_1 = datetime.strptime(spl[1], "%H:%M:%S")
                time_2 = datetime.strptime(spl2[1], "%H:%M:%S")
                timef = time_2 - time_1
                tiempomax = 3
                hf = str(timef).split(":")[0]
                if is_key(sumdic, pla.placa):
                    sumdic[pla.placa] = int(hf)
                else:
                    hft = sumdic[pla.placa]
                    hf = int(hf) + hft
                    sumdic[pla.placa] = int(hf)

                """check if is a employee"""
                if Vehiculo.vehiculo_usuario.through.objects.filter(vehiculo_id=placa.id_vehiculo_id).exists():
                    of = pla.vehiculo_usuario.through.objects.get(vehiculo_id=placa.id_vehiculo_id)
                    isof = Usuario.objects.get(id=of.usuario_id)
                    if isof.es_oficinista:
                        dic2["final"] = "permitido"
                    else:
                        if (tiempomax > int(hf)):
                            dic2["final"] = "permitido"
                        else:
                            if (tiempomax < int(hf)):
                                dic2["final"] = "excedido"
                else:
                    if (tiempomax >= int(hf)):
                        dic2["final"] = "permitido"
                    else:
                        if (tiempomax < int(hf)):
                            dic2["final"] = "excedido"
            temp_date = placa.hora_entrada
            datos.append(dic2)
        datosj = json.dumps(datos)
        return HttpResponse(datosj)

    return render(request, "Bitacora.html", DICT)


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def is_key(dict, val):
    if val in dict.keys():
        return False
    else:
        return True


def oficinistas(request):
    global DICT
    """Datos extraidos del servidor por medio de una consulta:
    [placa, num_oficina, nombre + apellido]"""
    logging.debug("Log message goes here.")
    datos = []
    pop = Vehiculo.objects.all();
    DICT["placas"] = pop
    c = Vehiculo.vehiculo_usuario.through.objects.all()
    for ad in c:
        dic2 = {}
        pla = Vehiculo.objects.get(id=ad.vehiculo_id)
        us = Usuario.objects.get(id=ad.usuario_id)
        dic2["placa"] = pla.placa
        dic2["oficinista"] = us.nombre
        dic2["oficina"] = us.num_oficina
        datos.append(dic2)
    DICT["datosServidor"] = datos
    return render(request, "Oficinistas.html", DICT)


def reportes(request):
    return render(request, "Reportes.html", DICT)
