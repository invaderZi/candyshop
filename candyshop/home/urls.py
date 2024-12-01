from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('acessardetalhes/<int:ProdutoCodigo>', views.acessardetalhes, name='acessardetalhes'),
    path('addfavorito/<int:ProdutoCodigo>', views.addfavorito, name='addfavorito'),
    path('addCarrinho/<int:ProdutoCodigo>', views.addCarrinho, name='addCarrinho'),
    path('search/', views.search, name='search'),
]
