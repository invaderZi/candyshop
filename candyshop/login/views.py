from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.contrib.messages import constants
from .models import CustomUser
from .backends import EmailBackend
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.mail import send_mail

def cadastro(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'cadastro.html')
    elif request.method == "POST":
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        telefone = request.POST.get('telefone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        
        if len(nome.strip()) == 0 or len(sobrenome.strip()) == 0 or len(telefone.strip()) == 0 or len(email.strip()) == 0 or len(password.strip()) == 0:
            messages.add_message(request, constants.ERROR,
                                 'Preencha todos os campos!')
            return redirect('/login/cadastro/')
        
        if not validate(email=email):
            messages.add_message(request, constants.ERROR,
                                 'O e-mail informado é inválido!')
            return redirect('/login/cadastro/')

        user = CustomUser.objects.filter(email=email)

        if user.exists():
            messages.add_message(request, constants.ERROR,
                                 'Já existe um usuário com esse e-mail cadastrado!')
            return redirect('/login/cadastro/')

        try:
            user = CustomUser.objects.create_user(
                username=nome, sobrenome=sobrenome, email=email, telefone=telefone, password=password)
            messages.add_message(request, constants.SUCCESS,
                                 'Cadastro realizado com sucesso')
            return redirect('/login/logar/')
        except Exception as ex:
            messages.add_message(request, constants.ERROR,
                                 f'Erro interno do sistema: {str(ex)}')
            return redirect('/login/cadastro/')

def recuperar(request):
    if request.method == "GET":        
        return redirect('/login/password_reset/')
    elif request.method == "POST":
        email = request.POST.get('email')
        send_mail(
            'Recuperação de conta',
            'Segue o e-mail de recuperação de conta solicitado! <br/> Clique aqui para recuperar sua conta!',
            '',
            [email],
            fail_silently=False,
        )
        messages.add_message(request, constants.SUCCESS,
                                 f'E-mail de redifinição de senha enviado com sucesso!')
        return redirect('/login/logar/')


def logar(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'logar.html')
    elif request.method == "POST":
        email = request.POST.get('email')
        senha = request.POST.get('password')

        usuario = EmailBackend.authenticate(email=email, password=senha)

        if not usuario:
            messages.add_message(request, constants.ERROR,
                                 'E-mail ou senha inválidos!')
            return redirect('/login/logar/')
        else:
            auth.login(request, usuario,backend='login.backends.EmailBackend')
            return redirect('/')


def sair(request):
    auth.logout(request)
    return redirect('/login/logar/')

def validate(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False
