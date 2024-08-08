from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from accounts.serializers import UserRegisterSerializer, LoginSerializer, UserSerializer

user_model = get_user_model()


class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = user_model.objects.create_user(username=username, email=email, password=password)
        user.save()
        data = UserSerializer(instance=user).data
        return Response({"message": "User created successfully", 'data': data}, status=status.HTTP_201_CREATED)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = authenticate(username=serializer.validated_data['username'], password=serializer.validated_data['password'])
        if user is not None:
            return Response({'message': 'Logged in successfully'}, status=status.HTTP_200_OK)
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

