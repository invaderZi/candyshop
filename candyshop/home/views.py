from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Produto, Favorito, Carrinho,ProdutoImagem,ItemCarrinho
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages import constants
from django.db.models import Q, F


@login_required(login_url='/login/logar/')
def home(request):
    produtos = Produto.objects.all()
    return render(request, 'home.html', {'produtos': produtos})


def acessardetalhes(request, ProdutoCodigo):
    produto = Produto.objects.get(ProdutoCodigo=ProdutoCodigo)
    return render(request, 'detalhesproduto.html', {'produto': produto})


def addfavorito(request, ProdutoCodigo):
    produto = Produto.objects.get(ProdutoCodigo=ProdutoCodigo)
    favoritos = Favorito.objects.filter(
        ClienteCodigo=request.user, ProdutoCodigo=produto)
    if not favoritos.exists():
        Favorito.objects.create(
            ClienteCodigo=request.user, ProdutoCodigo=produto)
        try:
            favorito_verificado = Favorito.objects.get(
                ClienteCodigo=request.user, ProdutoCodigo=produto)
            messages.add_message(request, constants.SUCCESS,
                                 'Favorito adicionado com sucesso!')
        except Favorito.DoesNotExist:
            messages.add_message(request, constants.ERROR,
                                 'Falha ao adicionar o favorito, favor tente novamente!')
    else:
        messages.add_message(request, constants.INFO,
                             'Favorito já adicionado!')
    return redirect(request.META.get('HTTP_REFERER', '/'))


def addCarrinho(request, ProdutoCodigo):
    produto = Produto.objects.get(ProdutoCodigo=ProdutoCodigo)
    carrinho = Carrinho.objects.filter(ClienteCodigo=request.user, Ativo=True).first()

    # Se o usuário não tem um carrinho ativo, crie um
    if not carrinho:
        carrinho = Carrinho.objects.create(ClienteCodigo=request.user, Ativo=True)

    item_carrinho = ItemCarrinho.objects.filter(CarrinhoCodigo=carrinho, ProdutoCodigo=produto).first()

    # Se o produto não está no carrinho, adicione-o
    if not item_carrinho:
        ItemCarrinho.objects.create(CarrinhoCodigo=carrinho, ProdutoCodigo=produto, Quantidade=1)
        messages.add_message(request, constants.SUCCESS, 'Produto adicionado ao carrinho!')
    else:
        # Se o produto já está no carrinho, aumente a quantidade
        item_carrinho.Quantidade = F('Quantidade') + 1
        item_carrinho.save()
        messages.add_message(request, constants.SUCCESS, 'Produto adicionado ao carrinho!')

    return redirect(request.META.get('HTTP_REFERER', '/'))

def search(request):
    text_search = request.POST.get('search')
    produtos = Produto.objects.filter(Q(ProdutoNome__icontains=text_search) | Q(
        ProdutoDescricao__icontains=text_search))
    return render(request, 'home.html', {'produtos': produtos})
