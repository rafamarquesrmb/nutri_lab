import re
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


def password_is_valid(request, password, confirm_password):
    if len(password) < 6:
        messages.add_message(request, constants.ERROR, 'Sua senha deve conter 6 ou mais caractertes')
        return False

    if not password == confirm_password:
        messages.add_message(request, constants.ERROR, 'As senhas não coincidem!')
        return False

    if not re.search('[A-Z]', password):
        messages.add_message(request, constants.ERROR, 'Sua senha não contem letras maiúsculas')
        return False

    if not re.search('[a-z]', password):
        messages.add_message(request, constants.ERROR, 'Sua senha não contem letras minúsculas')
        return False

    if not re.search('[1-9]', password):
        messages.add_message(request, constants.ERROR, 'Sua senha não contém números')
        return False

    return True


def username_is_valid(request, username):
    if len(username) < 3:
        messages.add_message(request, constants.ERROR, 'Seu usuário deve conter 3 ou mais caractertes')
        return False
    if User.objects.filter(username=username):
        messages.add_message(request, constants.ERROR, 'Usuário já cadastrado')
        return False
    return True


def email_is_valid(request, email):
    regex = re.compile(
        r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")
    if len(email) < 3:
        messages.add_message(request, constants.ERROR, 'Digite um email válido')
        return False
    if not re.fullmatch(regex, email):
        messages.add_message(request, constants.ERROR, 'Digite um email válido')
        return False
    if User.objects.filter(email=email):
        messages.add_message(request, constants.ERROR, 'Email já cadastrado')
        return False
    return True


def email_html(path_template: str, assunto: str, para: list, **kwargs) -> dict:
    html_content = render_to_string(path_template, kwargs)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(assunto, text_content, settings.EMAIL_HOST_USER, para)

    email.attach_alternative(html_content, "text/html")
    email.send()
    return {'status': 1}
