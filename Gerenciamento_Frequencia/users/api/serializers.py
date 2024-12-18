from rest_framework import serializers
from users.models import Funcionario, UserProfileExample


class UserProfileExampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfileExample
        fields = ['id', 'address', 'phone_number', 'birth_date', 'user']


class FuncionarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funcionario
        fields = "__all__"


class FuncionarioCreateSerializer(serializers.Serializer):
    nome = serializers.CharField(max_length=140)
    matricula = serializers.CharField(max_length=12)
    departamento = serializers.CharField(max_length=140)
    login = serializers.CharField(max_length=100)
    senha = serializers.CharField(max_length=100)

    def create(self, validated_data):
        # Cria o usuário
        user = user.objects.create_user(
            username=validated_data['login'],
            password=validated_data['senha']
        )

        # Cria o funcionário vinculado ao usuário
        funcionario = Funcionario.objects.create(
            nome=validated_data['nome'],
            matricula=validated_data['matricula'],
            departamento=validated_data['departamento'],
            user=user
        )
        return funcionario

    def update(self, instance, validated_data):
        """
        Atualiza os dados de um funcionário existente.
        """
        # Atualiza os campos básicos do funcionário
        instance.nome = validated_data.get('nome', instance.nome)
        instance.matricula = validated_data.get('matricula', instance.matricula)
        instance.departamento = validated_data.get('departamento', instance.departamento)

        # Atualiza o usuário vinculado, se necessário
        user_data = {
            'username': validated_data.get('login', instance.user.username),
            'password': validated_data.get('senha', None)  # Atualiza senha se fornecida
        }
        if user_data['username'] != instance.user.username:
            instance.user.username = user_data['username']
        if user_data['password']:
            instance.user.set_password(user_data['password'])
        instance.user.save()

        # Salva o funcionário atualizado
        instance.save()
        return instance
