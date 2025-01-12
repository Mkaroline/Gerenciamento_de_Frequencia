from django.contrib.auth.models import User, Group

from users.models import Funcionario  

class FuncionarioService:  

    def create(self, data):
        novo_user = User.objects.create_user(
                username=data['login'],
                password=data['senha'],
            )
        grupo_funcionarios, _ = Group.objects.get_or_create(name="Funcionarios")  
        novo_user.groups.add(grupo_funcionarios)

        novo_funcionario = Funcionario.objects.create( 
            nome=data['nome'],
            matricula=data['matricula'],
            departamento=data['departamento'],
            user=novo_user
        )
        return novo_funcionario
