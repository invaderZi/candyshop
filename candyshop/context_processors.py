from home.models import Favorito,Carrinho
from django.db.models import Sum
def qtd_favorite(request):
    # Obtenha o valor da quantidade de favoritos adicionado para o usuário logado
    qtd_favorite=0
    if request.user.is_authenticated:
        favoritos = Favorito.objects.filter(ClienteCodigo=request.user)
        qtd_favorite = len(favoritos)

    return {'qtd_favorite': qtd_favorite}

def qtd_cart(request):
    qtd_cart = 0
    if request.user.is_authenticated:
        carrinho = Carrinho.objects.filter(ClienteCodigo=request.user, Ativo=True).first()
        if carrinho:
            qtd_cart = carrinho.itens.count()

    return {'qtd_cart': qtd_cart}
