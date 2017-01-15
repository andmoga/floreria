from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Venta
from docxtpl import DocxTemplate
from cStringIO import StringIO

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
    
def factura(request):
    tpl = DocxTemplate('vidanueva/templates/docx/factura.docx')
    # todo las llaves se mantienen pero los valores deben ser datos dinamicos
    venta = Venta.objects.get(pk=1)
    context = {
        'fecha' : unicode(venta.fecha),
        'cliente' : unicode(venta.cliente),
        'documento' : venta.documento,
        'telefono' : 2222222,
        'ventas': [{'cantidad':venta.cantidad_arreglos, 'tipo_arreglo':venta.tipo_arreglo, 'precio':venta.valor_total, 'total':venta.cantidad_arreglos*venta.valor_total},{'cantidad':3, 'tipo_arreglo':'Flores feas', 'precio':10000, 'total':20000}],
        'total' : venta.valor_total,
        'iva' : '',
        'subtotal' : ''
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
    response['Content-Disposition'] = 'attachment; filename=factura'+str(venta.pk)+'.docx'
    response['Content-Length'] = length
    return response