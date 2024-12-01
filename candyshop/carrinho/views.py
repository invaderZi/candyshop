from django.shortcuts import render,redirect
from home.models import Carrinho,Produto
from django.contrib import messages
from django.contrib.messages import constants
from django.db.models import F,Sum
from .models import OpcaoEntrega,OpcaoPagamento,Pedidos
from home.models import ItemCarrinho
from perfil.models import CustomUser,Endereco
from django.core.mail import EmailMessage
import qrcode
from PIL import Image
import io
import base64
import os
from dotenv import load_dotenv
# Carrega as variáveis de ambiente
load_dotenv()


def carrinho(request):
    carrinho = Carrinho.objects.filter(ClienteCodigo=request.user, Ativo=True).first()
    if carrinho:
        itens_carrinho = carrinho.itens.all()
        total_carrinho = itens_carrinho.aggregate(total=Sum(F('Quantidade') * F('ProdutoCodigo__ProdutoValor')))['total']
    else:
        itens_carrinho = []
        total_carrinho = 0

    return render(request, 'carrinho.html', {'dados_carrinho': itens_carrinho, 'total_carrinho': total_carrinho})

def removecarrinho(request, ProdutoCodigo):
    produto = Produto.objects.get(ProdutoCodigo=ProdutoCodigo)
    carrinho = Carrinho.objects.filter(ClienteCodigo=request.user, Ativo=True).first()
    if carrinho:
        item_carrinho = ItemCarrinho.objects.filter(CarrinhoCodigo=carrinho, ProdutoCodigo=produto).first()
        if item_carrinho:
            item_carrinho.delete()
            messages.add_message(request, constants.SUCCESS, 'Produto removido do carrinho com sucesso!')
        else:
            messages.add_message(request, constants.ERROR, 'O produto não está no carrinho.')
    else:
        messages.add_message(request, constants.ERROR, 'Você não tem um carrinho ativo.')

    return redirect('carrinho')

def decrementaqtd(request, ProdutoCodigo):
    produto = Produto.objects.get(ProdutoCodigo=ProdutoCodigo)
    carrinho = Carrinho.objects.filter(ClienteCodigo=request.user, Ativo=True).first()
    if carrinho:
        item_carrinho = ItemCarrinho.objects.filter(CarrinhoCodigo=carrinho, ProdutoCodigo=produto).first()
        if item_carrinho and item_carrinho.Quantidade > 1:
            item_carrinho.Quantidade = F('Quantidade') - 1
            item_carrinho.save()

    return redirect('carrinho')

def incrementaqtd(request, ProdutoCodigo):
    produto = Produto.objects.get(ProdutoCodigo=ProdutoCodigo)
    carrinho = Carrinho.objects.filter(ClienteCodigo=request.user, Ativo=True).first()
    if carrinho:
        item_carrinho = ItemCarrinho.objects.filter(CarrinhoCodigo=carrinho, ProdutoCodigo=produto).first()
        if item_carrinho:
            item_carrinho.Quantidade = F('Quantidade') + 1
            item_carrinho.save()

    return redirect('carrinho')

def enderecos_entrega(request):   
    user = CustomUser.objects.filter(email=request.user.email).first()
    if user:
        enderecos = user.endereco_set.all()
        carrinho = Carrinho.objects.filter(ClienteCodigo=user, Ativo=True).first()
        opcao_entrega = None
        if carrinho:
            opcao_entrega = OpcaoEntrega.objects.filter(CarrinhoCodigo=carrinho).first()
    return render(request, 'enderecos_entrega.html', {'enderecos': enderecos, 'opcao_entrega': opcao_entrega})


def salvarretirada(request):
    if request.method == 'POST':
        opcao_selecionada = int(request.POST.get('entregar_retirar'))
        endereco_id = request.POST.get('endereco')
        if endereco_id == None and opcao_selecionada == 0:
            messages.add_message(request, constants.ERROR, 'Por favor para continuar selecione um endereço!')
            return redirect('enderecos_entrega')
        user = CustomUser.objects.filter(email=request.user.email).first()
        carrinho = Carrinho.objects.filter(ClienteCodigo=user, Ativo=True).first()  # pegue o carrinho ativo
        endereco = Endereco.objects.get(id=endereco_id) if opcao_selecionada == 0 else None

        opcao_entrega, created = OpcaoEntrega.objects.get_or_create(
            CarrinhoCodigo=carrinho,
            defaults={'OpcaoSelecionada': opcao_selecionada, 'EnderecoCodigo': endereco}
        )

        if not created:
            opcao_entrega.OpcaoSelecionada = opcao_selecionada
            opcao_entrega.EnderecoCodigo = endereco
            opcao_entrega.save() 

    return redirect('pagamentos') 

def pagamentos(request):
    user = CustomUser.objects.filter(email=request.user.email).first()
    carrinho = Carrinho.objects.filter(ClienteCodigo=user, Ativo=True).first()  # pegue o carrinho ativo
    opcao_entrega = OpcaoEntrega.objects.filter(CarrinhoCodigo=carrinho).first()  # pegue a OpcaoEntrega associada ao carrinho
    opcao_pagamento = None
    if opcao_entrega:
        opcao_pagamento = OpcaoPagamento.objects.filter(OpcaoEntregaCodigo=opcao_entrega).first()  # pegue a OpcaoPagamento associada à OpcaoEntrega
    return render(request, 'pagamento.html', {'opcao_pagamento': opcao_pagamento})  
def salvarpagamento(request):
    if request.method == 'POST':
        opcao_selecionada = int(request.POST.get('opcao_pagamento'))
        user = CustomUser.objects.filter(email=request.user.email).first()
        carrinho = Carrinho.objects.filter(ClienteCodigo=user, Ativo=True).first()  # pegue o carrinho ativo
        opcao_entrega = OpcaoEntrega.objects.filter(CarrinhoCodigo=carrinho).first()  # pegue a OpcaoEntrega associada ao carrinho

        if opcao_entrega:
            opcao_pagamento, created = OpcaoPagamento.objects.get_or_create(
                OpcaoEntregaCodigo=opcao_entrega,
                defaults={'OpcaoSelecionada': opcao_selecionada}
            )

            if not created:
                opcao_pagamento.OpcaoSelecionada = opcao_selecionada
                opcao_pagamento.save()

    return redirect('resumo_compra')  # substitua pelo nome da url para a qual você deseja redirecionar


def resumo_compra(request):
    user = CustomUser.objects.filter(email=request.user.email).first()
    carrinho = Carrinho.objects.filter(ClienteCodigo=user, Ativo=True).first()  # pegue o carrinho ativo
    itens_carrinho = ItemCarrinho.objects.filter(CarrinhoCodigo=carrinho)  # pegue os itens no carrinho
    total_pedido = sum(item.total_por_produto() for item in itens_carrinho)
    opcao_entrega = OpcaoEntrega.objects.filter(CarrinhoCodigo=carrinho).first()  # pegue a OpcaoEntrega associada ao carrinho
    opcao_pagamento = OpcaoPagamento.objects.filter(OpcaoEntregaCodigo=opcao_entrega).first() if opcao_entrega else None  # pegue a OpcaoPagamento associada à OpcaoEntrega
    
    context = {
        'user': user,
        'itens_carrinho': itens_carrinho,
        'total_pedido': total_pedido,
        'opcao_entrega': opcao_entrega,
        'opcao_pagamento': opcao_pagamento,
        'img_str': "data:image/png;base64,"+__genereateqrcode(total_pedido),
    }

    return render(request, 'resumo_compra.html', context)

def finalizarpedido(request):
    user = CustomUser.objects.filter(email=request.user.email).first()
    carrinho = Carrinho.objects.filter(ClienteCodigo=user, Ativo=True).first()  # pegue o carrinho ativo
    itens_carrinho = ItemCarrinho.objects.filter(CarrinhoCodigo=carrinho)  # pegue os itens no carrinho
    total_pedido = sum(item.total_por_produto() for item in itens_carrinho)
    opcao_entrega = OpcaoEntrega.objects.filter(CarrinhoCodigo=carrinho).first()
    opcao_pagamento = OpcaoPagamento.objects.filter(OpcaoEntregaCodigo=opcao_entrega).first() if opcao_entrega else None
    if carrinho:
        if opcao_pagamento.OpcaoSelecionada == 0:
            email = EmailMessage(
                'Seu boleto candyshop',
                f"""
                Olá,

                Aqui está o seu boleto:

                Nome: candyshop
                Valor: {total_pedido}
                Código de barras: ...

                Obrigado,
                Equipe candyshop
                """,
                'candyshop@candyshop.com',  # Substitua pelo seu e-mail
                [user.email],
            )

            # Envie o e-mail
            email.send()

        carrinho.Ativo = False  # altere o status para False
        carrinho.save()  # salve a alteração

        
        Pedido, created = Pedidos.objects.get_or_create(
                CarrinhoCodigo = carrinho,
                PorcentagemPedido=10,
                Cancelado = False
            )
        
        return redirect('pedidos')
        


def __genereateqrcode(value:float):
    
    # Crie uma instância QRCode
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    # Adicione dados ao QR Code
    qr.add_data('00020126390014BR.GOV.BCB.PIX0117teste@ninguem.com5204000053039865802BR5901N6001C62070503***6304A26E')
    qr.make(fit=True)

    # Crie uma imagem do QR Code
    img = qr.make_image(fill='black', back_color='white')

    # Converta a imagem em uma string base64
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    return base64.b64encode(buffer.getvalue()).decode()

def pedidos(request):
    user = CustomUser.objects.filter(email=request.user.email).first()
    carrinhos_fechados = Carrinho.objects.filter(ClienteCodigo=user, Ativo=False)
    pedidos = Pedidos.objects.filter(CarrinhoCodigo__in=carrinhos_fechados).order_by('-id')
    #opcao_entrega = {}
    #for pedido in pedidos:
        #pega a OpcaoEntrega para pedido que está vinculado ao carrinho
    #    opcao_entrega.pop(OpcaoEntrega.objects.filter(CarrinhoCodigo=pedido.CarrinhoCodigo).first())
    return render(request, 'pedidos.html',{'pedidos':pedidos})

def cancelapedido(request, id):
    pedido = Pedidos.objects.filter(id=id).first()
    if pedido:
        pedido.Cancelado = True
        pedido.PorcentagemPedido = 100
        pedido.save()
    
    return redirect(request.META.get('HTTP_REFERER', '/'))

def resumo_pedido(request,id):
    pedido = Pedidos.objects.filter(id=id).first()
    carrinho = pedido.CarrinhoCodigo
    itens_carrinho = ItemCarrinho.objects.filter(CarrinhoCodigo=carrinho)
    total_pedido = sum(item.total_por_produto() for item in itens_carrinho)
    opcao_entrega = OpcaoEntrega.objects.filter(CarrinhoCodigo=carrinho).first()
    opcao_pagamento = OpcaoPagamento.objects.filter(OpcaoEntregaCodigo=opcao_entrega).first() if opcao_entrega else None
    user = carrinho.ClienteCodigo

    context = {
        'user': user,
        'itens_carrinho': itens_carrinho,
        'total_pedido': total_pedido,
        'opcao_entrega': opcao_entrega,
        'opcao_pagamento': opcao_pagamento,
        'pedido': pedido,
    }

    return render(request, 'resumo_pedido.html', context)