from django.db import models
from perfil.models import Endereco
from home.models import Carrinho

# Create your models here.
class OpcaoEntrega(models.Model):
    OpcaoSelecionada = models.IntegerField(default=0)
    EnderecoCodigo = models.ForeignKey(Endereco, on_delete=models.CASCADE, null=True)
    CarrinhoCodigo = models.ForeignKey(Carrinho, on_delete=models.CASCADE)

class OpcaoPagamento(models.Model):
    OpcaoSelecionada = models.IntegerField(default=0)
    OpcaoEntregaCodigo = models.ForeignKey(OpcaoEntrega, on_delete=models.CASCADE)

class Pedidos(models.Model):
    PorcentagemPedido = models.IntegerField(default=0)
    Cancelado = models.BooleanField(default=False)
    CarrinhoCodigo = models.ForeignKey(Carrinho, on_delete=models.CASCADE)