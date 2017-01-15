from __future__ import unicode_literals

from django.db import models
import datetime

# Create your models here.

class TipoCliente(models.Model):
    texto = models.CharField(max_length=200)
    
    def __unicode__(self):
        return unicode(self.texto)

class Venta(models.Model):
    fecha = models.DateTimeField('Fecha de venta', default=datetime.datetime.now)
    tipo_arreglo = models.CharField('Tipo de arrelo', max_length=300)
    nombre_fallecido = models.CharField('Fallecido', max_length=300)
    cantidad_arreglos = models.IntegerField('Cantidad', default=1)
    cliente = models.CharField('Pedido por',max_length=300)
    tipo_cliente = models.ForeignKey(TipoCliente, null=False, blank=False)
    valor_total = models.IntegerField('Valor', null=False, blank=False)
    documento = models.IntegerField('Documento', null=True, blank=True)
    
    def __unicode__(self):
        return str(unicode(self.fecha.replace(tzinfo=None)) + ' - ' + unicode(self.cliente) + ' - ' + unicode(self.tipo_arreglo))