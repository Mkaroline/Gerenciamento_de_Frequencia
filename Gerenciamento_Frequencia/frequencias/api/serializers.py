from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from frequencias.models import FrequenciaModel, FuncionarioModel

"""classe frequencia Serializer"""


class FrequenciaSerializer(ModelSerializer):

    class Meta:
        model = FrequenciaModel
        fields = ["funcionario", "hora_inicio", "hora_fim"]


class FuncionarioSerializer(ModelSerializer):

    class Meta:
        model = FuncionarioModel
        fields = ['nome', 'matricula', 'departamento']
