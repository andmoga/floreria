from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(TipoCliente)
admin.site.register(Venta)