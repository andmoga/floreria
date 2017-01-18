from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^list$', views.list, name='list'),
    url(r'^factura/(?P<pk>\w+)$', views.factura, name='factura'),
    url(r'^factura/(?P<pk>\w+)/(?P<fechaInicial>\w+)/(?P<fechaFinal>\w+)$', views.facturaEntreFechas, name='facturaEntreFechas'),
]