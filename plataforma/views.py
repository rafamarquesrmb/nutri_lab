from datetime import datetime

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import constants
from django.views.decorators.csrf import csrf_exempt

from plataforma.utils import pacientes_validate, dados_paciente_validate
from plataforma.models import Pacientes, DadosPaciente


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


@login_required(login_url='/auth/logar')
def dados_paciente_listar(request):
    if request.method == "GET":
        pacientes_from_nutri = Pacientes.objects.filter(nutri=request.user)
        context = {
            'pacientes': pacientes_from_nutri
        }
        return render(request, 'dados_paciente_listar.html', context)


@login_required(login_url='/auth/logar')
def dados_paciente(request, id):
    paciente = Pacientes.objects.filter(id=id).filter(nutri=request.user).first()
    if not paciente:
        messages.add_message(request, constants.INFO, 'Paciente não encontrado...')
        return redirect('/dados_paciente/')

    if request.method == "GET":
        dados_paciente_list = paciente.dadospaciente_set.order_by('-data').all()
        context = {
            'paciente': paciente,
            'dados_paciente': dados_paciente_list
        }
        return render(request, 'dados_paciente.html', context)

    elif request.method == "POST":
        peso = request.POST.get('peso')
        altura = request.POST.get('altura')
        gordura = request.POST.get('gordura')
        musculo = request.POST.get('musculo')

        hdl = request.POST.get('hdl')
        ldl = request.POST.get('ldl')
        colesterol_total = request.POST.get('ctotal')
        trigliceridios = request.POST.get('trigliceridios')
        if not dados_paciente_validate(request, peso, altura, gordura, musculo, hdl,
                            ldl, colesterol_total, trigliceridios):
            return redirect(f'/dados_paciente/{paciente.id}')

        dados = DadosPaciente(paciente=paciente,
                                 data=datetime.now(),
                                 peso=peso,
                                 altura=altura,
                                 percentual_gordura=gordura,
                                 percentual_musculo=musculo,
                                 colesterol_hdl=hdl,
                                 colesterol_ldl=ldl,
                                 colesterol_total=colesterol_total,
                                 trigliceridios=trigliceridios)

        dados.save()

        messages.add_message(request, constants.SUCCESS, 'Dados cadastrado com sucesso')
        return redirect(f'/dados_paciente/{paciente.id}')


@login_required(login_url='/auth/logar/')
@csrf_exempt
def grafico_peso(request, id):
    paciente = Pacientes.objects.get(id=id)
    dados = paciente.dadospaciente_set.order_by('data').all()[:10]
    pesos = [dado.peso for dado in dados]
    # labels = list(range(len(pesos)))
    labels = [dado.data.strftime('%d/%m/%Y') for dado in dados]
    data = {'peso': pesos,
            'labels': labels}
    return JsonResponse(data)