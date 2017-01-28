from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Venta, Cliente, CantidadArreglo
from docxtpl import DocxTemplate
from cStringIO import StringIO
import datetime
import pytz

# Create your views here.

def index(request):
    template = loader.get_template('index.html')
    context = {
        'latest_question_list': '',
    }
    return HttpResponse(template.render(context, request))
    
def list(request):
    template = loader.get_template('list.html')
    context = {
        'ventas': Venta.objects.all(),
    }
    return HttpResponse(template.render(context, request))
    
def facturaFecha(request, pk):
    template = loader.get_template('facturaFecha.html')
    context = {
        'cliente': Cliente.objects.get(pk=pk),
    }
    return HttpResponse(template.render(context, request))
    
def factura(request, pk):
    tpl = DocxTemplate('vidanueva/templates/docx/factura.docx')
    # todo las llaves se mantienen pero los valores deben ser datos dinamicos
    cliente = Cliente.objects.get(pk=pk)
    ventas = Venta.objects.filter(cliente=cliente)
    arreglos_aux = []
    arreglos = CantidadArreglo.objects.filter(venta__cliente=cliente)
    subtotal = 0
    for arreglo in arreglos:
        arreglos_aux.append({ 'fecha':arreglo.venta.fecha.astimezone(pytz.timezone('America/Bogota')).strftime('%d-%m-%Y %H:%M'),
                            'cantidad':arreglo.cantidad,
                            'tipo_arreglo':arreglo.tipo_arreglo.nombre,
                            'nombre_fallecido':arreglo.venta.nombre_fallecido,
                            'total':arreglo.tipo_arreglo.precio*arreglo.cantidad})
        subtotal += arreglo.tipo_arreglo.precio*arreglo.cantidad
        
    context = {
        'fecha_actual' : unicode(datetime.datetime.now(pytz.timezone('America/Bogota')).strftime('%d-%m-%Y %H:%M')),
        'cliente' : unicode(cliente.nombre),
        'documento' : cliente.documento,
        'telefono' : cliente.telefono,
        'ventas': arreglos_aux,
        'total' : int(subtotal*1.19),
        'iva' : int(subtotal*0.19),
        'subtotal' : subtotal
    }

    tpl.render(context)
    f = StringIO()
    tpl.save(f)
    
    # descarga de documento
    length = f.tell()
    f.seek(0)
    response = HttpResponse(
        f.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )
    response['Content-Disposition'] = 'attachment; filename=factura'+str(cliente.pk)+'.docx'
    response['Content-Length'] = length
    return response
    
def facturaEntreFechas(request, pk, fechaInicial, fechaFinal):
    tpl = DocxTemplate('vidanueva/templates/docx/factura.docx')
    # todo las llaves se mantienen pero los valores deben ser datos dinamicos
    cliente = Cliente.objects.get(pk=pk)
    ventas = Venta.objects.filter(cliente=cliente, fecha__range=(datetime.datetime.strptime(fechaInicial, "%Y%m%d").date(), datetime.datetime.strptime(fechaFinal, "%Y%m%d").date()))
    arreglos_aux = []
    arreglos = CantidadArreglo.objects.filter(venta__in=ventas)
    subtotal = 0
    print ventas
    print arreglos
    for arreglo in arreglos:
        arreglos_aux.append({ 'fecha':arreglo.venta.fecha.astimezone(pytz.timezone('America/Bogota')).strftime('%d-%m-%Y %H:%M'),
                            'cantidad':arreglo.cantidad,
                            'tipo_arreglo':arreglo.tipo_arreglo.nombre,
                            'nombre_fallecido':arreglo.venta.nombre_fallecido,
                            'total':arreglo.tipo_arreglo.precio*arreglo.cantidad})
        subtotal += arreglo.tipo_arreglo.precio*arreglo.cantidad
        
    context = {
        'fecha_actual' : unicode(datetime.datetime.now(pytz.timezone('America/Bogota')).strftime('%d-%m-%Y %H:%M')),
        'cliente' : unicode(cliente.nombre),
        'documento' : cliente.documento,
        'telefono' : cliente.telefono,
        'ventas': arreglos_aux,
        'total' : int(subtotal*1.19),
        'iva' : int(subtotal*0.19),
        'subtotal' : subtotal
    }

    tpl.render(context)
    f = StringIO()
    tpl.save(f)
    
    # descarga de documento
    length = f.tell()
    f.seek(0)
    response = HttpResponse(
        f.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )
    response['Content-Disposition'] = 'attachment; filename=factura'+str(cliente.pk)+'.docx'
    response['Content-Length'] = length
    return response