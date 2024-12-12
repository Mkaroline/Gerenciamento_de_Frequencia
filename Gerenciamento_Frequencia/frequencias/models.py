"""teste"""
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
        """Meta informações do modelo."""
        verbose_name = "Frequência"
        verbose_name_plural = "Frequências"
