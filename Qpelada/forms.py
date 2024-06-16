from django import forms
from .models import UsuarioInfo, Peladas_bd, ListaDeJogadores, TrofeusBd

OPCOES_DIAS = [
    ("Segunda-feira", "Segunda-feira"),
    ("Terça-feira", "Terça-feira"),
    ("Quarta-feira", "Quarta-feira"),
    ("Quinta-feira", "Quinta-feira"),
    ("Sexta-feira", "Sexta-feira"),
    ("Sábado", "Sábado"),
    ("Domingo", "Domingo"),
]
OPCOES_POSICOES = [
    ('Atacante', 'Atacante'),
    ('Defensor', 'Defensor'),
    ('Goleiro', 'Goleiro'),
    ('Atacante ou defensor', 'Atacante ou defensor'),
    ('Atacante ou goleiro', 'Atacante ou goleiro'),
    ('Goleiro ou defensor', 'Goleiro ou defensor'),
    ('Qualquer posição', 'Qualquer posição'),
]
OPCOES_TROFEUS = [
    ('zero' , 0),
    (1 , 1),
    (2 , 2),
    (3 , 3),
    (4 , 4),
    (5 , 5),
]


class CriacaoPelada(forms.Form):
    imagem = forms.ImageField(
        required=True
    )
    nome = forms.CharField(
        label='Nome:',
        max_length= 100,
        required= True
    )
    campo = forms.CharField(
        label='Campo:',
        max_length= 100,
        required= True
    )
    preco = forms.FloatField(
       label='Preço:',
       required= True
    )
    dia = forms.ChoiceField(
        label='Dia:',
        choices=OPCOES_DIAS,
        required=True
    )
    hora = forms.TimeField(
        label='Horário:',
        required=True
    )
    regra = forms.CharField(
        label = 'Regras:',
        required = True,
        max_length=1000
    )
    exclude = ['pessoa', ]

class CriarPelada(forms.ModelForm):
    class Meta:
        model = Peladas_bd
        exclude = ['usuario','nota']
        fields = "__all__"
        widgets = {
            'foto': forms.FileInput({'class':'btn-img', 'label':'Imagem'}),
            'nome': forms.TextInput({'class':'input-nome'}),
            'campo': forms.TextInput({'class':'input-campo'}),
            'preço': forms.NumberInput({'class':'input-preco'}),
            'dia': forms.Select({'class':'dia-selecao'}),
            'hora': forms.TimeInput({'class':'input-hora'}),
            'regra': forms.Textarea({'class':'input-regra'}),
            
        }

class ListaForms(forms.ModelForm):
    class Meta:
        model = ListaDeJogadores
        exclude = ['dono','jogador','numero',]
        fields = {}

class TrofeusForms(forms.ModelForm):
    class Meta:
        model = TrofeusBd
        exclude = ['pelada', 'eleitor',]
        fields = "__all__"
        widgets = {
            'trofeus': forms.Select({'class':'any'}),
        }

class EditarPerfil(forms.ModelForm):
    class Meta:
        model = UsuarioInfo
        exclude = ['pessoa',]
        fields = '__all__'
        widgets = {
            'imagem': forms.FileInput({'class':'input-img'}),
            'posicao': forms.Select({'class':'input-posi'}),
            'sobre': forms.Textarea({'class':'input-sobre'}),
        }





    # imagem = forms.ImageField(
    #     required=True
    # )
    # posicao = forms.ChoiceField(
    #     label='Posição:',
    #     choices=OPCOES_POSICOES,
    #     required=True
    # )
    # sobre = forms.CharField(
    #     label='Sobre:',
    #     required = True,
    #     max_length=1000
    # )