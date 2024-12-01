from django.db import models
from login.models import CustomUser
class Endereco(models.Model):
    ESTADOS_CHOICES = [
        ('12', 'Acre'),
        ('27', 'Alagoas'),
        ('16', 'Amapá'),
        ('13', 'Amazonas'),
        ('29', 'Bahia'),
        ('23', 'Ceará'),
        ('53', 'Distrito Federal'),
        ('32', 'Espírito Santo'),
        ('52', 'Goiás'),
        ('21', 'Maranhão'),
        ('51', 'Mato Grosso'),
        ('50', 'Mato Grosso do Sul'),
        ('31', 'Minas Gerais'),
        ('15', 'Pará'),
        ('25', 'Paraíba'),
        ('41', 'Paraná'),
        ('26', 'Pernambuco'),
        ('22', 'Piauí'),
        ('33', 'Rio de Janeiro'),
        ('24', 'Rio Grande do Norte'),
        ('43', 'Rio Grande do Sul'),
        ('11', 'Rondônia'),
        ('14', 'Roraima'),
        ('42', 'Santa Catarina'),
        ('35', 'São Paulo'),
        ('28', 'Sergipe'),
        ('17', 'Tocantins')
    ]


    rua = models.CharField(max_length=255)
    numero = models.IntegerField()
    cep = models.CharField(max_length=8)
    estado = models.CharField(max_length=2, choices=ESTADOS_CHOICES)
    cidade = models.CharField(max_length=255)
    complemento = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
