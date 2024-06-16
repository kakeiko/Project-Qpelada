from django.db import models
from django.contrib.auth.models import User

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
    ('0' , '0'),
    ('1' , '1'),
    ('2' , '2'),
    ('3' , '3'),
    ('4' , '4'),
    ('5' , '5'),
]

class Peladas_bd(models.Model):
    foto = models.ImageField(upload_to="fotos/", blank=False)
    nome = models.CharField(max_length=100, null=False, blank=False)
    campo = models.CharField(max_length=100, null=False, blank=False)
    preço = models.FloatField(max_length=100, null=False, blank=False)
    dia = models.CharField(max_length=100, choices=OPCOES_DIAS, default='')
    hora = models.TimeField(blank=False, null=False)
    regra = models.CharField(max_length=1000, blank=False,null=False)
    usuario = models.ForeignKey(to= User, on_delete=models.CASCADE, null=True, blank=False, related_name="User")
    nota = models.FloatField(max_length=100, null=True, blank=True)

class UsuarioInfo(models.Model):
    imagem = models.ImageField(upload_to="fotos/")
    posicao = models.CharField(max_length=100, choices=OPCOES_POSICOES, default='')
    sobre = models.CharField(max_length= 1000)
    pessoa = models.ForeignKey(to= User, on_delete=models.CASCADE, null=True, blank=False, related_name="pessoa")

class ListaDeJogadores(models.Model):
    dono = models.ForeignKey(to= Peladas_bd, on_delete=models.CASCADE, null= True, blank=False, related_name="dono")
    jogador = models.ForeignKey(to = User, on_delete=models.CASCADE, null=True, blank=False, related_name='jogadores')
    numero = models.IntegerField(null=True , blank=False)

class TrofeusBd(models.Model):
    pelada = models.ForeignKey(to= Peladas_bd, on_delete=models.CASCADE, null=True, blank=False, related_name="pelada")
    eleitor = models.ForeignKey(to = User, on_delete=models.CASCADE, null=True, blank=False, related_name='eleitor')
    trofeus = models.CharField(max_length=100, choices=OPCOES_TROFEUS, default='')