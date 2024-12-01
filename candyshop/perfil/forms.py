from django import forms
from .models import Endereco
from login.models import CustomUser

class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = ['rua', 'numero', 'cep', 'estado', 'cidade','complemento']


        
