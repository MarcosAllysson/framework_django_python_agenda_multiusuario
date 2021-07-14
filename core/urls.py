from django.urls import path
from django.views.generic import RedirectView
from .views import (
    lista_eventos,
    json_lista_eventos,
    evento,
    submit_evento,
    delete_evento,
    login_user,
    submit_login,
    logout_user
)


urlpatterns = [
    path('', RedirectView.as_view(url='/agenda/')),
    path('agenda/', lista_eventos),
    path('agenda/lista/', json_lista_eventos),
    path('agenda/evento/', evento),
    path('agenda/evento/submit', submit_evento),
    path('agenda/evento/delete/<int:id_evento>/', delete_evento),

    # caso usuário não esteja logado, redireciona-o
    path('login/', login_user),
    path('login/submit', submit_login),
    path('logout/', logout_user)
]
