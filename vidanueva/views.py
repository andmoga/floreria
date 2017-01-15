from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Venta

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