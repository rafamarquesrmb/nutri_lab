from django.contrib import messages
from django.contrib.messages import constants

from plataforma.models import Pacientes, DadosPaciente


def pacientes_validate(request, nome, sexo, idade, email, telefone):
    if (len(nome.strip()) == 0) or (len(sexo.strip()) == 0) or (len(idade.strip()) == 0) or (
            len(email.strip()) == 0) or (len(telefone.strip()) == 0):
        messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
        return False

    if not idade.isnumeric():
        messages.add_message(request, constants.ERROR, 'Digite uma idade válida')
        return False

    pacientes = Pacientes.objects.filter(email=email)
    # TODO: a verificação só deve ser aplicada para os pacientes do usuário.
    # TODO: Em caso de outro usuário, pode cadastrar um e-mail similar.
    if pacientes.exists():
        messages.add_message(request, constants.ERROR, 'Já existe um paciente com esse E-mail')
        return False

    return True


def dados_paciente_validate(request, peso, altura, percentual_gordura, percentual_musculo, colesterol_hdl,
                            colesterol_ldl, colesterol_total, trigliceridios):
    if not (
            peso.isnumeric()
            and altura.isnumeric()
            and percentual_gordura.isnumeric()
            and percentual_musculo.isnumeric()
            and colesterol_hdl.isnumeric()
            and colesterol_ldl.isnumeric()
            and colesterol_total.isnumeric()
            and trigliceridios.isnumeric()):
        messages.add_message(request, constants.ERROR, 'É necessário preencher todos os dados.')
        return False
    return True
