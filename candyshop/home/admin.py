from django.contrib import admin
from .models import Produto,Favorito,ProdutoImagem,Carrinho,ItemCarrinho
# Register your models here.

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('ProdutoCodigo', 'ProdutoNome', 'ProdutoValor')
    list_display_links = ('ProdutoCodigo', 'ProdutoNome')

@admin.register(ProdutoImagem)
class ProdutoImagemAdmin(admin.ModelAdmin):
    list_display = ('produto','imagem')
    list_display_links = ('produto','imagem')

@admin.register(Favorito)
class FavoritoAdmin(admin.ModelAdmin):
    list_display = ('FavoritoCodigo', 'ClienteCodigo', 'ProdutoCodigo')
    list_display_links = ('FavoritoCodigo', 'ClienteCodigo')

@admin.register(Carrinho)
class CarrinhoAdmin(admin.ModelAdmin):
    list_display = ('CarrinhoCodigo', 'ClienteCodigo', 'Ativo')
    list_display_links = ('CarrinhoCodigo', 'ClienteCodigo', 'Ativo')

@admin.register(ItemCarrinho)
class ItemCarrinhoAdmin(admin.ModelAdmin):
    list_display = ('id', 'CarrinhoCodigo', 'ProdutoCodigo', 'Quantidade')
    list_display_links = ('id', 'CarrinhoCodigo', 'ProdutoCodigo')





