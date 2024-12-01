from django.db import models
from django.conf import settings


        
class Produto(models.Model):
    ProdutoCodigo = models.AutoField(primary_key=True)
    ProdutoNome = models.CharField(max_length=55)
    ProdutoDescricao = models.CharField(max_length=2000)
    ProdutoValor = models.FloatField()

    def __str__(self):
        return f"{self.ProdutoCodigo} - {self.ProdutoNome}"

class ProdutoImagem(models.Model):
    produto = models.ForeignKey(Produto, related_name='imagens', on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='produtos/', default='')

    def __str__(self):
        return f"{self.produto.ProdutoNome} Imagem ID {self.id}"
    
class Favorito(models.Model):
    FavoritoCodigo = models.AutoField(primary_key=True)
    ClienteCodigo = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ProdutoCodigo = models.ForeignKey(Produto, on_delete=models.CASCADE)

class Carrinho(models.Model):
    CarrinhoCodigo = models.AutoField(primary_key=True)
    ClienteCodigo = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Ativo = models.BooleanField(default=True)
    

class ItemCarrinho(models.Model):
    CarrinhoCodigo = models.ForeignKey(Carrinho, related_name='itens', on_delete=models.CASCADE)
    ProdutoCodigo = models.ForeignKey(Produto, on_delete=models.CASCADE)
    Quantidade = models.IntegerField()

    def total_por_produto(self):
        return self.ProdutoCodigo.ProdutoValor * self.Quantidade
    def qtd_itens(self):
        return self.itens.count()