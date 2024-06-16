from django import forms


class LoginForm(forms.Form):
    nome = forms.CharField(
        label='Nome do Usuário',
        max_length= 100,
        required= True
    )
    senha = forms.CharField(
        label='Senha',
        max_length= 16,
        required= True,
        widget=forms.PasswordInput()
    )

class CadastroForms(forms.Form):
    nome_cadastro = forms.CharField(
        label='Nome do Usuário',
        max_length= 100,
        required= True
    )
    email = forms.EmailField(
        label='E-mail',
        max_length= 200,
        required= True
    )
    senha_cadastro = forms.CharField(
        label='Senha',
        max_length= 16,
        required= True,
        widget=forms.PasswordInput()
    )
    confirm_senha = forms.CharField(
        label='Confirme sua senha',
        max_length= 16,
        required= True,
        widget=forms.PasswordInput()
    )