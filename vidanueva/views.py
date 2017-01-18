from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Venta, Cliente
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
    
def factura(request, pk):
    tpl = DocxTemplate('vidanueva/templates/docx/factura.docx')
    # todo las llaves se mantienen pero los valores deben ser datos dinamicos
    cliente = Cliente.objects.get(pk=pk)
    ventas = Venta.objects.filter(cliente=cliente)
    ventas_aux = []
    subtotal = 0
    for venta in ventas:
        ventas_aux.append({ 'fecha':venta.fecha.astimezone(pytz.timezone('America/Bogota')).strftime('%d-%m-%Y %H:%M'),
                            'cantidad':venta.cantidad_arreglos,
                            'tipo_arreglo':venta.tipo_arreglo,
                            'nombre_fallecido':venta.nombre_fallecido,
                            'total':venta.valor_total})
        subtotal += venta.valor_total
        
    context = {
        'fecha_actual' : unicode(datetime.datetime.now(pytz.timezone('America/Bogota')).strftime('%d-%m-%Y %H:%M')),
        'cliente' : unicode(cliente.nombre),
        'documento' : cliente.documento,
        'telefono' : cliente.telefono,
        'ventas': ventas_aux,
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