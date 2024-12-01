from django.contrib import admin
from .models import OpcaoEntrega

# Register your models here.

@admin.register(OpcaoEntrega)
class OpcaoEntregaAdmin(admin.ModelAdmin):
    list_display = ('OpcaoSelecionada', 'EnderecoCodigo', 'CarrinhoCodigo')
    list_display_links = ('OpcaoSelecionada', 'EnderecoCodigo', 'CarrinhoCodigo')
