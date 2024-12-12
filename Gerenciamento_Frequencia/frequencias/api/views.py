""" Comentario para ser erro """
import logging
from datetime import datetime
from rest_framework import status
from rest_framework.exceptions import PermissionDenied, NotAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from frequencias.api.serializers import FrequenciaSerializer
from frequencias.models import FrequenciaModel

logger = logging.getLogger("frequencias")


class FrequenciaViewSet(ModelViewSet):
    """ViewSet para manipulação das instacias"""
    serializer_class = FrequenciaSerializer
    permission_classes = [AllowAny]
    queryset = FrequenciaModel.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = FrequenciaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            funcionario = serializer.validated_data['funcionario']
            hora_atual = datetime.now()

            frequencia_existe = FrequenciaModel.objects.filter(
                funcionario=funcionario,
                hora_fim=None).exists()

            if not frequencia_existe:
                raise ValueError
            else:
                nova_frequencia = FrequenciaModel.objects.create(
                    funcionario=funcionario,
                    hora_inicio=hora_atual,
                    hora_fim=None
                )

                serializer_saida = FrequenciaSerializer(nova_frequencia)
                logger.info("Frequência Criada!")
                return Response(
                    {"Info": "Frequência iniciada com sucesso!",
                     "data": serializer_saida.data},
                    status=status.HTTP_201_CREATED)

        except KeyError:
            return Response({"Erro": "Dados faltando ou incorretos."},
                            status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied:
            return Response(
                {"Erro": "Você não possui permissões para isso."},
                status=status.HTTP_403_FORBIDDEN)
        except ValueError:
            logger.error("Frequencia já esta cadastrada")
            return Response(
                {"Info": "Esta Frequência já foi cadastrada antes!"},
                status=status.HTTP_409_CONFLICT)
        except Exception:
            return Response(
                {"Erro": "Erro ao criar frequência."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        try:
            frequencia = self.get_object()
            frequencia.hora_fim = datetime.now()
            frequencia.save()

            serializer_saida = FrequenciaSerializer(frequencia)
            return Response({"Info": "Frequência atualizada com sucesso!",
                             "data": serializer_saida.data},
                            status=status.HTTP_200_OK)
        except ValueError:
            logger.error("Frequencia inválida.")
            return Response(
                {"Erro": "Dados da frenquencia inválidos!"},
                status=status.HTTP_409_CONFLICT)
        except KeyError:
            return Response(
                {"Erro": "Algum dado da frwquencia faltando ou errado."},
                status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied:
            return Response(
                {"Erro": "Você não possui permissões para isso."},
                status=status.HTTP_403_FORBIDDEN)
        except NotAuthenticated:
            return Response(
                {"Erro": "Usuário não autenticado."},
                status=status.HTTP_401_UNAUTHORIZED)
