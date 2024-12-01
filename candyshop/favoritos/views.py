from django.shortcuts import render,redirect
from home.models import Produto, Favorito
from django.contrib import messages
from django.contrib.messages import constants

# Create your views here.


def favoritos(request):
    # Obtenha todos os favoritos para esse usuário
    favoritos = Favorito.objects.filter(ClienteCodigo=request.user)

    # Obtenha todos os produtos que estão nos favoritos
    produtos_favoritos = [favorito.ProdutoCodigo for favorito in favoritos]

    return render(request, 'favoritos.html', {'produtos': produtos_favoritos})


def removefavorito(request, ProdutoCodigo):
    try:
        favorito = Favorito.objects.get(
            ClienteCodigo=request.user, ProdutoCodigo=ProdutoCodigo)
        favorito.delete()
        messages.add_message(request, constants.SUCCESS,
                             'Produto removido dos favoritos com sucesso!')
        
        return redirect('favoritos')
    except Favorito.DoesNotExist:
        messages.add_message(request, constants.ERROR,
                             'Falha ao remover o favorito, favor tentar novamente!')
