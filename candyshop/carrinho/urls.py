from django.urls import path
from . import views
urlpatterns = [
    path('', views.carrinho, name='carrinho'),
    path('removecarrinho/<int:ProdutoCodigo>', views.removecarrinho, name='removecarrinho'),
    path('decrementaqtd/<int:ProdutoCodigo>', views.decrementaqtd, name='decrementaqtd'),
    path('incrementaqtd/<int:ProdutoCodigo>', views.incrementaqtd, name='incrementaqtd'),
    path('enderecos_entrega', views.enderecos_entrega, name='enderecos_entrega'),
    path('salvarretirada', views.salvarretirada, name='salvarretirada'),
    path('pagamentos', views.pagamentos, name='pagamentos'),
    path('salvarpagamento', views.salvarpagamento, name='salvarpagamento'),
    path('resumo_compra', views.resumo_compra, name='resumo_compra'),
    path('finalizarpedido', views.finalizarpedido, name='finalizarpedido'),
    path('pedidos', views.pedidos, name='pedidos'),
    path('cancelapedido/<int:id>', views.cancelapedido, name='cancelapedido'),
    path('resumo_pedido/<int:id>', views.resumo_pedido, name='resumo_pedido'),
    
]
