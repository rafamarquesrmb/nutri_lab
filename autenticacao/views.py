from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from autenticacao.utils import password_is_valid, email_is_valid, username_is_valid


# Create your views here.
def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    elif request.method == "POST":
        usuario = request.POST.get('usuario')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')
        if (not password_is_valid(request, senha, confirmar_senha) or not email_is_valid(
                request, email) or not username_is_valid(request, username=usuario)):
            return redirect('/auth/cadastro')

        try:
            user = User.objects.create_user(username=usuario,
                                            email=email,
                                            password=senha,
                                            is_active=False)
            user.save()
            return redirect('/auth/logar')
        except:
            return redirect('/auth/cadastro')


def logar(request):
    return HttpResponse("Página de logar")
