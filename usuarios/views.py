from django.shortcuts import render, redirect
from usuarios.forms import LoginForm, CadastroForms
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib import messages
from Qpelada.models import UsuarioInfo

def login_pg(request):
    form = LoginForm
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():

            nome = form['nome'].value()
            senha = form['senha'].value()

        usuario = auth.authenticate(
            request,
            username=nome,
            password=senha
        )
        
        

        if usuario is not None:
            auth.login(request, usuario)
            messages.success(request, "Parabêns logado com sucesso!")
            
            if not UsuarioInfo.objects.filter(pessoa = usuario.id).exists():
                usuario_info = UsuarioInfo.objects.create(
                    pessoa = request.user
                )

                usuario_info.save()
                return redirect('home')

            return redirect('home')
        else:
            messages.error(request, 'Ops, algo de errado não está certo!')
            return redirect('login')

        



    return render(request, 'pag-login.html', {"form": form})

def cadastro_pg(request):
    form = CadastroForms

    if request.method == 'POST':
        form = CadastroForms(request.POST)

        if form.is_valid():
            senha_verificar = form['senha_cadastro'].value()
            senha_confirmar = form['confirm_senha'].value()
            # if  senha_verificar != form['confirm_senha'].value():
            #     messages.error(request, 'As senhas estão diferentes!')
            #     return redirect('cadastro')
            # if len( senha_verificar) < 8:
            #     messages.error(request, 'A senha tem que conter no minímo 8 dígitos.')
            #     return redirect('cadastro')
            VerificaSenha(senha_verificar, senha_confirmar, request)
            
            nome = form['nome_cadastro'].value()
            email = form['email'].value()
            senha = form['senha_cadastro'].value()

            if User.objects.filter(username = nome).exists():
                messages.error(request,'Esse nome de usuário já existe!')
                return redirect('cadastro')

            usuario = User.objects.create_user(
                username = nome,
                email= email,
                password= senha
            )
                
            usuario.save()
                
            messages.success(request, 'Cadastro concluído!') 
            return redirect('login')
            

    return render(request, 'pag-cadastro.html', {"form": form})

def logout(request):
    auth.logout(request)
    messages.success(request,"Logout efetuado com sucesso!")
    return redirect('home')

def VerificaSenha(senha, confirm_senha, request):
    lMaisc, lMins, number, length = 0, 0, 0, 0
    length = len(senha)
    
    if  senha != confirm_senha:
        messages.error(request, 'As senhas estão diferentes!')
        return redirect('cadastro')
    if len(senha) < 8:
        messages.error(request, 'A senha tem que conter no minímo 8 dígitos.')
        return redirect('cadastro')
    else:
        for i in range(0, length):
            if senha[i].isupper():
                lMaisc += 1
            elif senha[i].islower():
                lMins += 1
            elif senha[i].isdigit():
                number += 1
    if lMaisc != 0 and lMins != 0 and number != 0 :
            return True
    else:
        messages.error(request, 'A senha deve conter, letras maiúsculas, minúsculas e números')