from __future__ import unicode_literals

from django.db import models
from django.contrib import admin
from django.utils.html import format_html
import datetime

# Create your models here.


class TipoCliente(models.Model):
    texto = models.CharField(max_length=200)
    
    def __unicode__(self):
        return unicode(self.texto)

class Cliente(models.Model):
    nombre = models.CharField('Pedido por',max_length=300)
    tipo_cliente = models.ForeignKey(TipoCliente, null=False, blank=False)
    documento = models.IntegerField('Documento', null=True, blank=True)
    telefono = models.IntegerField('Telefono', null=True, blank=True)
    def __unicode__(self):
        return unicode(self.nombre)
        
    def imprimir(self):
        return format_html(
            '<a href="https://floristeria-andmoga.c9users.io/vidanueva/factura/{}" class="btn btn-default">Imprimir</a>',
            self.pk
        )

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'nombre', 'tipo_cliente', 'documento', 'telefono', 'imprimir')

class TipoArreglo(models.Model):
    nombre = models.CharField('Tipo de arreglo', max_length=300)
    precio = models.IntegerField('Valor', null=False, blank=False)
    
    def __unicode__(self):
        return unicode(self.nombre)

class Venta(models.Model):
    fecha = models.DateTimeField('Fecha de venta', default=datetime.datetime.now)
    arreglos = models.ManyToManyField(TipoArreglo, through='CantidadArreglo')
    nombre_fallecido = models.CharField('Fallecido', max_length=300)
    cliente = models.ForeignKey(Cliente, null=False, blank=False)
    
    def __unicode__(self):
        return str(unicode(self.fecha.replace(tzinfo=None)) + ' - ' + unicode(self.cliente) + ' - ' + unicode(self.nombre_fallecido))
        
    class Meta:
        ordering = ['-fecha']
        

class CantidadArreglo(models.Model):
    venta = models.ForeignKey(Venta)
    tipo_arreglo = models.ForeignKey(TipoArreglo)
    cantidad = models.IntegerField('Cantidad', default=1)
    
    def __unicode__(self):
        return unicode(self.venta) + ' - ' + unicode(self.cantidad) + ' - ' + unicode(self.tipo_arreglo)