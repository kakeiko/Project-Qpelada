from django.urls import path
from usuarios.views import login_pg, cadastro_pg, logout


urlpatterns = [
    path('login/', login_pg, name='login'),
    path('cadastrar/', cadastro_pg, name='cadastro'),
    path('logout/', logout, name="logout")
]