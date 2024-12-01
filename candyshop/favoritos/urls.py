from django.urls import path
from . import views
urlpatterns = [
    path('', views.favoritos, name='favoritos'),
    path('removefavorito/<int:ProdutoCodigo>', views.removefavorito, name='removefavorito'),

]
