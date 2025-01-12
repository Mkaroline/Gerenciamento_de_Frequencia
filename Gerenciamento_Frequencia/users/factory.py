import random
from faker import Faker
from django.contrib.auth.models import User

from users.models import Funcionario  
fake = Faker('pt_BR')

class FuncionarioFactory:

    def create_user(self):
        new_user = User.objects.create_user(
            username=fake.user_name(),
            password=fake.password()
        )
        return new_user

    def create(self):
        novo_funcionario = Funcionario.objects.create( 
            nome=fake.name(),
            matricula=random.randint(300, 500),
            departamento=fake.job(),
            user=self.create_user()
        )
        return novo_funcionario

    def create_multiple(self, num):
        for _ in range(0, num):
            self.create()