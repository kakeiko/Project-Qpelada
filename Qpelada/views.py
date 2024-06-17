from django.shortcuts import render, get_object_or_404, redirect
from Qpelada.models import Peladas_bd, UsuarioInfo, ListaDeJogadores, TrofeusBd
from .filters import PeladasFilter
from .forms import EditarPerfil, CriarPelada, ListaForms, TrofeusForms
from django.contrib import messages
from django.contrib.auth.models import User
from datetime import date



def index(request):
    if str(request.user) == 'AnonymousUser':
        nome_login = {"nome": 'Login'}
    else:
        nome_login = {"nome": str(request.user)}

    if request.user.is_authenticated:    
        user = request.user
        usuario = UsuarioInfo.objects.filter(pessoa__exact = user)
    else:
        usuario = UsuarioInfo.objects.filter(pessoa__exact = '3')

    dia = date.today().weekday()
    nomes = ('Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo')
    dia_semana = nomes[dia]

    jogos = Peladas_bd.objects.all().order_by('-nota')
    jogos_hoje = Peladas_bd.objects.filter(dia = dia_semana)
    return render(request, 'index.html', {"cards": jogos, "nome": nome_login, "user": usuario, 'cards2': jogos_hoje})

def peladas(request):
    if str(request.user) == 'AnonymousUser':
        nome_login = {"nome": 'Login'}
    else:
        nome_login = {"nome": str(request.user)}
    
    if request.user.is_authenticated:    
        user = request.user
        usuario = UsuarioInfo.objects.filter(pessoa__exact = user)
    else:
        usuario = UsuarioInfo.objects.filter(pessoa__exact = '3')

    jogos = Peladas_bd.objects.all()
    jogo_filtro = PeladasFilter(request.GET, jogos)
    print(PeladasFilter())

    return render(request, 'pag-peladas.html', {"cards": jogo_filtro.qs, "filter": jogo_filtro, "nome": nome_login, "user": usuario})

def criar(request):
    if str(request.user) == 'AnonymousUser':
        nome_login = {"nome": 'Login'}
    else:
        nome_login = {"nome": str(request.user)}
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.user.is_authenticated:    
        user = request.user
        usuario = UsuarioInfo.objects.filter(pessoa__exact = user)
    else:
        usuario = UsuarioInfo.objects.filter(pessoa__exact = '3')

    jogos = Peladas_bd.objects.filter(usuario__exact = request.user)
    return render(request, 'pag-criar.html', {"cards": jogos, "nome": nome_login, "user": usuario})

def pelada(request, jogo_id):
    if str(request.user) == 'AnonymousUser':
        nome_login = {"nome": 'Login'}
    else:
        nome_login = {"nome": str(request.user)}

    if request.user.is_authenticated:    
        user = request.user
        usuario = UsuarioInfo.objects.filter(pessoa__exact = user)
    else:
        usuario = UsuarioInfo.objects.filter(pessoa__exact = '3')

    jogospeladas = get_object_or_404(Peladas_bd, pk=jogo_id)
    form = ListaForms
    lista = ListaDeJogadores.objects.filter(dono = jogo_id)
    
    if request.method == 'POST':
        form = ListaForms(request.POST)
        nome_lista = ListaDeJogadores.objects.filter(dono = jogospeladas, jogador = request.user)
        if nome_lista.exists():
            messages.error(request, 'Seu nome já está na lista')
            return redirect('pelada', jogo_id)
        else:
            if form.is_valid():
                criar_lista = form.save(commit=False)
                criar_lista.dono = jogospeladas
                criar_lista.jogador = request.user
                if ListaDeJogadores.objects.filter(dono = jogo_id) == 0 : 
                    criar_lista.numero = len(lista) + 2
                else:
                    criar_lista.numero = len(lista) + 1
                criar_lista.save()
                
                
                messages.success(request, 'Nome adicionado')
                return redirect('pelada', jogo_id)
        
       
        
    return render(request, 'pelada-ind.html', {'form': form, "pelada": jogospeladas, "nome": nome_login, "user": usuario, "list": lista})

def avaliacao(request, jogo_id):
    if str(request.user) == 'AnonymousUser':
        nome_login = {"nome": 'Login'}
    else:
        nome_login = {"nome": str(request.user)}

    if request.user.is_authenticated:    
        user = request.user
        usuario = UsuarioInfo.objects.filter(pessoa__exact = user)
    else:
        usuario = UsuarioInfo.objects.filter(pessoa__exact = '3')

    peladabd = Peladas_bd.objects.get(pk = jogo_id)
    form_pelada = CriarPelada(instance=peladabd)
    jogospeladas = get_object_or_404(Peladas_bd, pk=jogo_id)
    form = TrofeusForms
    avaliacoes = TrofeusBd.objects.filter(pelada = jogospeladas)
    soma_nota = 0
    

    if request.method == 'POST':
        form = TrofeusForms(request.POST)
        form_pelada = CriarPelada(request.POST, request.FILES, instance=peladabd)
        form_validacao = TrofeusBd.objects.filter(pelada = jogospeladas, eleitor = request.user)
        if form_validacao.exists():
            messages.error(request, 'Você ja avaliou essa pelada!')
            return redirect('pelada', jogo_id)
        else:
            if form.is_valid() and form_pelada.is_valid():
                criar_trofeu = form.save(commit=False)
                criar_trofeu.pelada = jogospeladas
                criar_trofeu.eleitor = request.user
                criar_trofeu.save()
                for item in avaliacoes:
                    soma_nota += int(item.trofeus)
        
                nota = soma_nota / len(avaliacoes)
                criar_nota = form_pelada.save(commit=False)
                criar_nota.nota = nota
                criar_nota.save()
                messages.success(request, 'Pelada avaliada!')
                return redirect('pelada', jogo_id)        

    return render(request, 'pag-avaliacao.html', {'form': form, "pelada": jogospeladas, "nome": nome_login, "user": usuario, 'formP':form_pelada} )

def lista_deletar(request, jogo_id):
    lista = ListaDeJogadores.objects.filter(dono = jogo_id)
    lista.delete()
    messages.success(request, 'Lista deletada')
    return redirect('peladae', jogo_id)

def peladaE(request, jogo_id):
    if str(request.user) == 'AnonymousUser':
        nome_login = {"nome": 'Login'}
    else:
        nome_login = {"nome": str(request.user)}

    if request.user.is_authenticated:    
        user = request.user
        usuario = UsuarioInfo.objects.filter(pessoa__exact = user)
    else:
        usuario = UsuarioInfo.objects.filter(pessoa__exact = '3')

    jogos = Peladas_bd.objects.filter(pk = jogo_id)
    jogospeladas = get_object_or_404(Peladas_bd, pk=jogo_id)
    form = ListaForms
    lista = ListaDeJogadores.objects.filter(dono = jogo_id)

    if request.method == 'POST':
        form = ListaForms(request.POST)
        if form.is_valid():
            criar_lista = form.save(commit=False)
            criar_lista.dono = jogospeladas
            criar_lista.jogador = request.user
            if ListaDeJogadores.objects.filter(dono = jogo_id) == 0 : 
                criar_lista.numero = len(lista) + 2
            else:
                criar_lista.numero = len(lista) + 1
            criar_lista.save()
            messages.success(request, 'Nome adicionado')
            return redirect('peladae', jogo_id)
    return render(request, 'pelada-ind-edit.html', {'form': form, "pelada": jogospeladas, "nome": nome_login, "user": usuario, "cards": jogos, "list": lista})

def criacao(request):
    if str(request.user) == 'AnonymousUser':
        nome_login = {"nome": 'Login'}
    else:
        nome_login = {"nome": str(request.user)}
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.user.is_authenticated:    
        user = request.user
        usuario = UsuarioInfo.objects.filter(pessoa__exact = user)
    else:
        usuario = UsuarioInfo.objects.filter(pessoa__exact = '3')

    form = CriarPelada


    if request.method == 'POST':
        form = CriarPelada(request.POST, request.FILES)
        if form.is_valid():
            criar_pelada = form.save(commit=False)
            criar_pelada.usuario = request.user
            criar_pelada.save()
            messages.success(request, 'Pelada criada!')
            return redirect('criar')
   
    return render(request, 'parte-criacao.html', {'form': form, "nome": nome_login, "user": usuario})

def pelada_editar(request, jogo_id):

    if str(request.user) == 'AnonymousUser':
        nome_login = {"nome": 'Login'}
    else:
        nome_login = {"nome": str(request.user)}

    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.is_authenticated:    
        user = request.user
        usuario = UsuarioInfo.objects.filter(pessoa__exact = user)
    else:
        usuario = UsuarioInfo.objects.filter(pessoa__exact = '3')
    
    peladabd = Peladas_bd.objects.get(pk = jogo_id)
    form = CriarPelada(instance=peladabd)

    if request.method == 'POST':
        form = CriarPelada(request.POST, request.FILES, instance=peladabd)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pelada editado com sucesso')
            return redirect('criar')

    jogospeladas = get_object_or_404(Peladas_bd, pk=jogo_id)
    return render(request, 'parte-pelada-editar.html', {"pelada": jogospeladas, 'form': form, "nome": nome_login, "user": usuario})

def pelada_deletar(request, jogo_id):
    jogo = Peladas_bd.objects.get(id=jogo_id)
    jogo.delete()
    messages.success(request, 'Pelada deletada')
    return redirect('criar')

def perfil(request):
    if str(request.user) == 'AnonymousUser':
        nome_login = {"nome": 'Login'}
    else:
        nome_login = {"nome": str(request.user)}

    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.is_authenticated:    
        user = request.user
        usuario = UsuarioInfo.objects.filter(pessoa__exact = user)
    else:
        usuario = UsuarioInfo.objects.filter(pessoa__exact = '3')

    return render(request, 'pag-perfil.html', {"nome": nome_login, "user": usuario, "user": usuario})
    
def perfil_editar(request, user_id):

    if str(request.user) == 'AnonymousUser':
        nome_login = {"nome": 'Login'}
    else:
        nome_login = {"nome": str(request.user)}

    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.is_authenticated:    
        user = request.user
        usuario = UsuarioInfo.objects.filter(pessoa__exact = user)
    else:
        usuario = UsuarioInfo.objects.filter(pessoa__exact = '3')

    

    pessoabd = UsuarioInfo.objects.get(pessoa = request.user)
    form = EditarPerfil(instance=pessoabd)

    if request.method == 'POST':
        form = EditarPerfil(request.POST, request.FILES, instance=pessoabd)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil editado com sucesso')
            return redirect('perfil')
    

    return render(request, 'pag-perfil-editar.html', {"nome": nome_login, "user": usuario, "user": usuario, 'form': form, 'user_id': user_id})

def perfil_deletar(request):
    usuarioD = request.user
    perfilD = User.objects.get(username = usuarioD)
    perfilD.delete()
    messages.success(request, 'Perfil deletado')
    return redirect('login')
