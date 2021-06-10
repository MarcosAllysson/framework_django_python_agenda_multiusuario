from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


# Create your models here.
class Evento(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    data_evento = models.DateTimeField(verbose_name='Data do Evento')
    data_criacao = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        #  especificando qual nome da tabela
        db_table = 'evento'

    def __str__(self):
        return self.titulo

    def get_data_criacao(self):
        """
        Método que formata a data e hora e retorna no modelo brasileiro dd/mm/aaaa H:M
        """
        return self.data_evento.strftime('%d/%m/%Y %H:%M')

    def get_data_input_evento(self):
        """
        Método que retorna formato de hora pra alteração de dados.
        """
        return self.data_evento.strftime('%Y-%m-%dT%H:%M')

    def get_evento_atrasado(self):
        """
        Método que retorna qual evento está atrasado
        """
        if self.data_evento < datetime.now():
            return True
        else:
            return False
