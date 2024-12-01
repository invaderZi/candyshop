from django.shortcuts import render,redirect, get_object_or_404
from login.models import CustomUser  # ou o nome do seu modelo de Perfil
from .forms import EnderecoForm
from .models import Endereco
import requests
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.messages import constants

def perfil(request):
    user = CustomUser.objects.filter(email=request.user.email).first()
    if user:
        enderecos = user.endereco_set.all()
    return render(request, 'perfil.html', {'perfil': user, 'enderecos': enderecos})

def endereco_view(request, endereco_id=None):
    if endereco_id:
        endereco = get_object_or_404(Endereco, id=endereco_id)
    else:
        endereco = Endereco()

    form = EnderecoForm(request.POST or None, instance=endereco)

    if form.is_valid():
        endereco = form.save(commit=False)  # Não salve o formulário ainda
        endereco.user = request.user  # Defina o usuário do endereço como o usuário atual
        endereco.save()  # Agora salve o formulário
        messages.add_message(request, constants.SUCCESS,
                             'Endereço salvo com sucesso!')
        return redirect('perfil')  
        
    return render(request, 'add_enderecos.html', {'form': form,'endereco_id': endereco_id})


def get_cidades(request, uf):
    response = requests.get(f'https://servicodados.ibge.gov.br/api/v1/localidades/estados/{uf}/distritos')
    return JsonResponse(response.json(), safe=False)

def delete(request, endereco_id=None):
    try:
        endereco = get_object_or_404(Endereco, id=endereco_id)
        endereco.delete()
        messages.add_message(request, constants.SUCCESS,
                             'Endereço removido com sucesso!')
        return redirect('perfil')  
    except Endereco.DoesNotExist:
        messages.add_message(request, constants.ERROR,
                             'Falha ao remover o endereço, favor tentar novamente!')
        return redirect('perfil')  

def salvarperfil(request, perfil_id):
    if request.method == "POST":
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        telefone = request.POST.get('telefone')
        email = request.POST.get('email')

        user = CustomUser.objects.filter(id=perfil_id).first()
        if user:
            user.username = nome
            user.sobrenome = sobrenome
            user.telefone = telefone
            user.email = email
            user.save()
            messages.add_message(request, constants.SUCCESS, 'Perfil atualizado com sucesso!')
        else:
            messages.add_message(request, constants.ERROR,
                             'Falha ao tentar atualizar o usuário, favor tente novamente!')
    return redirect('perfil') 
        

        
    