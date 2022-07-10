from django.contrib import admin
from plataforma.models import Pacientes, DadosPaciente, Opcao, Refeicao

admin.site.register(Pacientes)
admin.site.register(DadosPaciente)
admin.site.register(Refeicao)
admin.site.register(Opcao)