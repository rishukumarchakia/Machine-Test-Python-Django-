from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Client, Project

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class ClientSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'created_at', 'created_by', 'updated_at']  

class ProjectCreateSerializer(serializers.ModelSerializer):
    users =serializers.PrimaryKeyRelatedField(queryset =User.objects.all(),many=True)

    class meta:
        model =Project
        fields = ['id', 'project_name', 'client', 'users', 'created_at', 'created_by']

    def create(self, validated_data):
        users = validated_data.pop('users')
        project = Project.objects.create(**validated_data)
        project.users.set(users)
        return project

class ProjectSerializer(serializers.ModelSerializer):
    client = serializers.StringRelatedField(read_only=True)
    users = UserSerializer(many=True, read_only=True)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'client', 'users', 'created_at', 'created_by']
