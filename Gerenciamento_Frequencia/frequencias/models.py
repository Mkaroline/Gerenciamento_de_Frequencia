from datetime import datetime
from django.db import models
from users.models import Funcionario


class FrequenciaModel(models.Model):
    """Modelo que representa a frequência."""
    hora_inicio = models.DateTimeField(default=datetime.now)
    hora_fim = models.DateTimeField(null=True, blank=True)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)

    def __str__(self):
        return (
            f"Funcionário: [{self.funcionario}] - Frequência: "
            f"[{self.hora_inicio}] - [{self.hora_fim}]"
        )

    class Meta:
        verbose_name = "Frequência"
        verbose_name_plural = "Frequências"


class FuncionarioModel(models.Model):
    """Modelo que representa o Funcionário"""
    nome = models.CharField(max_length=140)
    matricula = models.CharField(max_length=12)
    departamento = models.CharField(max_length=140)

    def __str__(self):
        return f'Funcionario - Frequencia[{self.nome}] - [{self.matricula}]'

    class Meta:
        verbose_name = "Funcionario"
        verbose_name_plural = "Funcionarios"
