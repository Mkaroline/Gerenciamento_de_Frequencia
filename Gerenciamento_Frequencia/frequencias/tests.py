from django.test import TestCase
from rest_framework import status
from frequencias.models import FuncionarioModel, FrequenciaModel
from rest_framework.authtoken.models import Token

from rest_framework.test import APIClient

class FrequenciaTesteCase(TestCase):
    def setUp(self):
        self.nova_frequencia = FrequenciaModel.objects.create(
            hora_inicio= "2024-12-03T15:29:05Z",
            hora_fim = "2024-12-12T14:44:58.469601Z",
            funcionario = 4
        )
      
        self.new_user = User.objects.create_user(username="admin",password="adminadmin")
        self.new_user.is_staff = True
        self.new_user.is_superuser = True
        self.new_user.save()
        self.token, _ = Token.objects.get_or_create(user=self.new_user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_cadastrar_frequencias(self):
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
        
    def test_listar_frequencias(self):
        url = "http://localhost:8000/frequencias/"
        FrequenciaModel.objects.create(
            funcionario =  4,
		    hora_inicio = "2024-12-03T15:29:05Z",
		    hora_fim =  "2024-12-12T14:44:58.469601Z"
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['funcionario'], 4)
    
    def test_atualizar_frequencias(self):
        url = f"http://localhost:8000/frequencias/{self.nova_frequencias.id}/"
        data = {
            "funcionario": 9,
	        "hora_inicio": "2024-12-04T16:18:20Z",
		    "hora_fim": "2024-12-19T19:48:18.974368Z"
        }
        response = self.client.put(url,data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_deletar_frequencias(self):
        url = f"http://localhost:8000/frequencias/{self.nova_frequencias.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(FrequenciaModel.objects.filter(id=self.nova_frequencias.id).exists())
        
    def test_cadastrar_funcionario(self):
        url = "http://localhost:8000/funcionarios/"
        
        funcionario_data = {
            "id": 7,
            "nome": "Lavinia",
            "matricula": "123456789123",
            "departamento": "Power BI",
            "user": 7
        }

        data = {
            "hora_inicio": "2025-01-12T08:00:00Z",
            "hora_fim": "2025-01-12T12:00:00Z",
            "funcionario": funcionario_data["id"]
        }

        # Primeiro POST - funcionário válido
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(FuncionarioModel.objects.filter(hora_inicio="2025-01-12T08:00:00Z").exists())
        
   
    def test_listar_funcionarios(self):
        url = "http://localhost:8000/funcionarios/"
        
        FuncionarioModel.objects.create(
            id=7,
            nome="Lavinia",
            matricula="123456789123",
            departamento="Power BI",
            user=7,
            hora_inicio="2025-01-12T08:00:00Z",
            hora_fim="2025-01-12T12:00:00Z"
        )

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['nome'], "Lavinia")
        self.assertEqual(response.data[0]['matricula'], "123456789123")
        
    def test_atualizar_funcionario(self):
        url = f"http://localhost:8000/funcionarios/{self.novo_funcionario.id}/"
        FuncionarioModel.objects.create(
        id = 9,
		nome = "Maria Silva",
		matricula = "54321",
		departamento = "RH",
		user = 9
    )
        data = {
        "funcionario": 9,
		"hora_inicio": "2024-12-04T16:18:20Z",
		"hora_fim": "2024-12-19T20:00:52.237593Z"
        }
        response = self.client.put(url,data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_deletar_funcionario(self):
        url = f"http://localhost:8000/funcionarios/{self.novo_funcionario.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(FuncionarioModel.objects.filter(id=self.novo_funcionario.id).exists())

            
            
