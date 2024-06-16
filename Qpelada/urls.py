from django.urls import path
from Qpelada.views import index, peladas, criar, pelada, criacao, perfil, perfil_editar, pelada_editar, peladaE, pelada_deletar, perfil_deletar, lista_deletar, avaliacao

urlpatterns = [
    path('', index, name='home'),
    path('peladas/', peladas, name='peladas'),
    path('criar/', criar, name='criar'),
    path('pelada/<int:jogo_id>', pelada, name='pelada'),
    path('criação/', criacao, name='criacao'),
    path('perfil', perfil, name='perfil'),
    path('perfil/editar/<int:user_id>', perfil_editar, name='editarP'),
    path('pelada/editar/<int:jogo_id>', pelada_editar, name='editarpelada'),
    path('peladaE/<int:jogo_id>', peladaE, name='peladae'),
    path('pelada/deletar/<int:jogo_id>', pelada_deletar, name='deletarpelada'),
    path('perfil/deletar', perfil_deletar, name='deletarperfil'),
    path('perfil/deletarLista/<int:jogo_id>', lista_deletar, name='deletarlista'),
    path('pelada/avaliar/<int:jogo_id>', avaliacao, name='avaliar'),
]