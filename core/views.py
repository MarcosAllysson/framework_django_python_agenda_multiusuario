from django.shortcuts import render, HttpResponse, redirect
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime, timedelta
from django.http.response import Http404, JsonResponse


def login_user(request):
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('/')


# usuário logado
def submit_login(request):
    if request.POST:
        # recuperando imput de dados do form no html na página de login
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('/')
        else:
            #  se o usuário não conseguir autenticar, printa mensagem de erro
            messages.error(request, 'Usuário ou senha inválido.')

    return redirect('/')

# só acessa quem estiver logado. Se não estiver, redireciona para login/
@login_required(login_url='/login/')
def lista_eventos(request):
    #  pra listar somente do usuário logado
    usuario = request.user
    data_atual = datetime.now() - timedelta(hours=1)
    evento = Evento.objects.filter(usuario=usuario,
                                   data_evento__gt=data_atual)
    dados = {'eventos': evento}

    #  pra listar só 1
    #evento = Evento.objects.get(id=1)

    #  pra listar todos
    #evento = Evento.objects.all()
    #dados = {'eventos': evento}
    return render(request, 'agenda.html', dados)


@login_required(login_url='/login/')
def evento(request):
    #  pegando id pra alteração
    id_evento = request.GET.get('id')
    dados = {}
    if id_evento:
        dados['evento'] = Evento.objects.get(id=id_evento)
    return render(request, 'evento.html', dados)


@login_required(login_url='/login/')
def submit_evento(request):
    if request.POST:
        #  obtendo todos os valores digitados no form da página evento
        titulo = request.POST.get('titulo')
        data_evento = request.POST.get('data_evento')
        descricao = request.POST.get('descricao')
        usuario = request.user
        id_evento = request.POST.get('id_evento')

        #  pra alterar invés de registrar
        if id_evento:
            evento = Evento.objects.get(id=id_evento)

            #  assim consigo validar se quem está alterando é de fato o dono. Além de poder validar se houve alteração.
            if evento.usuario == usuario:
                evento.titulo = titulo
                evento.descricao = descricao
                evento.data_evento = data_evento
                evento.save()

            #  outra maneira:
            #Evento.objects.filter(id=id_evento).update(titulo=titulo,
            #                                           data_evento=data_evento,
            #                                           descricao=descricao)
        else:
            #  registrar
            Evento.objects.create(titulo=titulo,
                                  data_evento=data_evento,
                                  descricao=descricao,
                                  usuario=usuario)

    #  depois de criado, redireciona para a página principal
    return redirect('/')


@login_required(login_url='/login/')
def delete_evento(request, id_evento):
    usuario = request.user

    try:
        evento = Evento.objects.get(id=id_evento)
    except Exception:
        raise Http404()

    #  pra fazer com que apenas o dono do evento possa deletar o evento.
    if usuario == evento.usuario:
        evento.delete()
    else:
        #  se não for deletado, levanta um error 404
        raise Http404()
    return redirect('/')


@login_required(login_url='/login/')
def json_lista_eventos(request):
    usuario = request.user
    evento = Evento.objects.filter(usuario=usuario).values('id', 'titulo')

    return JsonResponse(list(evento), safe=False)


#def index(request):
#    """
#    View para redirecionar o usuário quando tentar acessar url vazio ''
#    """
#    return redirect('/agenda/')