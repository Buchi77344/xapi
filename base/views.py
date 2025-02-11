from django.shortcuts import render ,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from django.contrib import auth
from rest_framework.permissions import IsAuthenticated ,IsAdminUser


from .models import CustomUser

class SignupView(APIView):
   
    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        password = request.data.get("password")

        if not username or not email or not password:
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        if CustomUser.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        if CustomUser.objects.filter(email=email).exists():
            return Response({"error": "Email already registered"}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.create_user(username=email, email=email, password=password,first_name=first_name,last_name=last_name)
        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)


from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status



class Login(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=email, password=password)  # Change username=email to work with email-based login
        if user is not None:
            login(request, user)
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


class logoutapi(APIView):
    def post(self,request):
        auth.logout(request)
        return Response({"message":"logout successfully"},status=status.HTTP_200_OK)

class Detail(APIView):
 
    def get(self, request, pk):
        # Fetch user or return 404 if not found
        user = get_object_or_404(CustomUser, pk=pk)
        
        # Use the serializer to convert the user object to JSON format
        serializer = Usersignupserializer(user)
        
        # Return the serialized data as the response
        return Response(serializer.data)
    
class UserList(APIView):
    def get(self, request):
        # Fetch all users from the CustomUser model
        users = CustomUser.objects.all() 
        
        # Serialize the list of users 
        serializer = Usersignupserializer(users, many=True)  # `many=True` is for a list of objects
        
        # Return serialized data as response
        return Response(serializer.data)


class CreateTodo(APIView):
    permission_classes = [IsAuthenticated]
    def post(self ,request):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class ListTodo(APIView):

    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
             todo = Todo.objects.all()

             serializer =  TodoSerializer(todo, many=True)
             return  Response(serializer.data,status=status.HTTP_200_OK)
        except Todo.DoesNotExist:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
    


class UpdateTodo(APIView):
    permission_classes = [IsAuthenticated]
    def put(self,request,pk):
        try:
            todo = get_object_or_404(Todo, pk=pk)
        except Todo.DoesNotExist:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
        
        seriaizer = TodoSerializer(todo ,data =request.data)

        if seriaizer.is_valid():
            seriaizer.save()
            return Response( seriaizer.data, status=status.HTTP_200_OK)
        
        return Response( seriaizer.errors, status=status.HTTP_404_NOT_FOUND)
    def patch(self,request,pk):
        permission_classes = [IsAuthenticated]
        try :
            todos = get_object_or_404(Todo, pk=pk)

        except Todo.DoesNotExist:
             return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer =  TodoSerializer(todos,data=request.data , partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response( serializer.data, status=status.HTTP_200_OK)
        return Response( serializer.errors, status=status.HTTP_404_NOT_FOUND)
    

class Delatetodo(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self,request,pk):
        try:
            delete = get_object_or_404(Todo,pk=pk)
        except Todo.DoesNotExist:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
        delete.delete()
        return Response({"message": "Task deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
            
        



