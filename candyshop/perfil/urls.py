from django.urls import path
from . import views
urlpatterns = [
    path('', views.perfil, name='perfil'),
    path('endereco/<int:endereco_id>/', views.endereco_view, name='endereco'),
    path('delete/<int:endereco_id>/', views.delete, name='delete'),
    
    path('add_endereco/<int:endereco_id>/', views.endereco_view, name='add_endereco'),
    path('get_cidades/<str:uf>/', views.get_cidades, name='get_cidades'),
    path('salvarPerfil/<int:perfil_id>/', views.salvarperfil, name='salvarPerfil')
]
