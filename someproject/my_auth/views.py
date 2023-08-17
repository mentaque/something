import random
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login, authenticate, logout
from someproject.tasks import send_email
from .models import CustomUser
from .serializers import UserSerializer, UserRegistrationSerializer, UserLoginSerializer, UserCheckingLoginSerializer


@swagger_auto_schema(method='POST', request_body=UserRegistrationSerializer)
@api_view(['POST'])
@permission_classes([AllowAny])
def user_registration(request):
    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='POST', request_body=UserLoginSerializer)
@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user:
            verification_code = random.randint(100000, 999999)
            user.verification_code = verification_code
            user.save()
            send_email.delay(email, str(verification_code))
            return Response({'detail': 'verification code was sent'}, status=status.HTTP_200_OK)
        return Response({'detail': 'Invalid data'}, status=status.HTTP_401_UNAUTHORIZED)


@swagger_auto_schema(method='POST', request_body=UserCheckingLoginSerializer)
@api_view(['POST'])
@permission_classes([AllowAny])
def checking_login(request):
    if request.method == 'POST':
        email = request.data.get('email')
        code = request.data.get('verification_code')
        try:
            user = CustomUser.objects.get(email=email)
        except:
            return Response({'detail': 'something went wrong'})
        if not user.verification_code:
            return Response({'detail': 'Invalid data #0'}, status=status.HTTP_401_UNAUTHORIZED)
        if user.verification_code == code:
            login(request, user)
            serializer = UserSerializer(user)
            user.verification_code = 0
            user.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid data'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return Response({'detail': 'Successfully logged out'})


@swagger_auto_schema(method='PUT', request_body=UserRegistrationSerializer)
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)