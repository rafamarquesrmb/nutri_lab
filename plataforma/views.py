from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import constants

from plataforma.utils import pacientes_validate
from plataforma.models import Pacientes


@login_required(login_url='/auth/logar/')
def pacientes(request):
    if request.method == "GET":
        pacientes_from_nutri = Pacientes.objects.filter(nutri=request.user)
        context = {
            'pacientes': pacientes_from_nutri
        }
        return render(request, 'pacientes.html', context)
    elif request.method == "POST":
        nome = request.POST.get("nome")
        sexo = request.POST.get("sexo")
        idade = request.POST.get("idade")
        email = request.POST.get("email")
        telefone = request.POST.get("telefone")

        if not pacientes_validate(request, nome, sexo, idade, email, telefone):
            return redirect('/pacientes/')

        try:
            paciente = Pacientes(nome=nome,
                                 email=email,
                                 sexo=sexo,
                                 idade=idade,
                                 telefone=telefone,
                                 nutri=request.user)
            paciente.save()
            messages.add_message(request, constants.SUCCESS, 'Paciente cadastrado com sucesso!')
            return redirect('/pacientes/')
        except:
            messages.add_message(request, constants.ERROR,
                                 'Erro ao tentar adicionar o paciente... Tente novamente mais tarde.')
            return redirect('/pacientes/')
