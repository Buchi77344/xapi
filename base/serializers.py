from rest_framework import serializers
from base.models import CustomUser ,Todo

class Usersignupserializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    class Meta:
        model = CustomUser
        fields = '__all__'

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model =Todo
        fields = "__all__"
    
    def create(self,validated_data):
        todo = Todo.objects.create(
            name =validated_data['name'],
            email =validated_data['email'],
            subject =validated_data['subject'],
        )
        return todo