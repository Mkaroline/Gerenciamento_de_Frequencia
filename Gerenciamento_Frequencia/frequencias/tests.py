from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from rest_framework import status



from frequencias.models import FrequenciaModel

# Create your tests here.

class FrequenciaTesteCase(TestCase):

    def setUp(self):
        pass

    def test_cadastrar_frequencia(self):
        url = "http://localhost:8000/frequencias/"
        data = {
            "hora_inicio": "2024-12-03T15:29:05Z",
            "hora_fim": "2024-12-12T14:44:58.469601Z",
            "funcionario": 4
        }
        response = self.client.post(url,data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(FrequenciaModel.objects.filter(hora_inicio= "2024-12-03T15:29:05Z",
        hora_fim = "2024-12-12T14:44:58.469601Z", funcionario = 4).exists())

        response = self.client.post(url,data)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
    