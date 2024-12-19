import logging
from datetime import datetime
from rest_framework import status
from rest_framework.exceptions import PermissionDenied, NotAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from frequencias.api.serializers import FrequenciaSerializer
from frequencias.models import FrequenciaModel

logger = logging.getLogger("frequencias")

class FrequenciaViewSet(ModelViewSet):
    """ViewSet para manipulação das instâncias de Frequência."""
    serializer_class = FrequenciaSerializer
    permission_classes = [IsAuthenticated]
    queryset = FrequenciaModel.objects.all()

    def get_permissions(self):
        """
        Define permissões diferentes dependendo da ação executada.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]  # Apenas administradores podem criar, atualizar ou excluir
        return super().get_permissions()  # Permissões padrão para outras ações

    def create(self, request, *args, **kwargs):
        """
        Cria uma nova Frequência para um Funcionário.
        Verifica se já não existe uma frequência em aberto para o mesmo funcionário.
        """
        serializer = FrequenciaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            funcionario = serializer.validated_data['funcionario']
            hora_atual = datetime.now()

            # Verifica se o funcionário já tem uma frequência aberta (sem hora de fim)
            frequencia_existe = FrequenciaModel.objects.filter(
                funcionario=funcionario,
                hora_fim=None).exists()

            if frequencia_existe:
                return Response(
                    {"Info": "Esta Frequência já foi cadastrada antes!"},
                    status=status.HTTP_409_CONFLICT
                )

            # Cria a nova frequência
            nova_frequencia = FrequenciaModel.objects.create(
                funcionario=funcionario,
                hora_inicio=hora_atual,
                hora_fim=None
            )

            serializer_saida = FrequenciaSerializer(nova_frequencia)
            logger.info("Frequência Criada!")
            return Response(
                {"Info": "Frequência iniciada com sucesso!", "data": serializer_saida.data},
                status=status.HTTP_201_CREATED
            )

        except KeyError:
            return Response({"Erro": "Dados faltando ou incorretos."},
                            status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied:
            return Response(
                {"Erro": "Você não possui permissões para isso."},
                status=status.HTTP_403_FORBIDDEN)
        except ValueError:
            logger.error("Frequência já está cadastrada")
            return Response(
                {"Info": "Esta Frequência já foi cadastrada antes!"},
                status=status.HTTP_409_CONFLICT
            )

    def update(self, request, *args, **kwargs):
        """
        Atualiza a hora de fim da Frequência, marcando como finalizada.
        """
        try:
            frequencia = self.get_object()  # Obtém o objeto de frequência a ser atualizado
            frequencia.hora_fim = datetime.now()  # Marca o fim da frequência
            frequencia.save()

            serializer_saida = FrequenciaSerializer(frequencia)
            return Response({"Info": "Frequência atualizada com sucesso!",
                             "data": serializer_saida.data},
                            status=status.HTTP_200_OK)
        except ValueError:
            logger.error("Frequência inválida.")
            return Response(
                {"Erro": "Dados da frequência inválidos!"},
                status=status.HTTP_409_CONFLICT)
        except KeyError:
            return Response(
                {"Erro": "Algum dado da frequência faltando ou errado."},
                status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied:
            return Response(
                {"Erro": "Você não possui permissões para isso."},
                status=status.HTTP_403_FORBIDDEN)
        except NotAuthenticated:
            return Response(
                {"Erro": "Usuário não autenticado."},
                status=status.HTTP_401_UNAUTHORIZED)
