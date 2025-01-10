from frequencias.models import FrequenciaModel

class FrequenciaService:

    def create(self, data):
        hora_inicio = data['hora_inicio']
        hora_fim = data['hora_fim']

        in_database = FrequenciaModel.objects.filter(
            hora_inicio=hora_inicio,
            hora_fim=hora_fim).exists()

        if in_database:
            raise ValueError
        else:
         nova_frequencia = FrequenciaModel.objects.create( 
            hora_inicio=data['hora_inicio'],
            hora_fim=data['hora_fim'],
            funcionario=data['funcionario']
    )
        return nova_frequencia_
