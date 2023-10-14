from django.contrib.auth.models import User
from .models import Package, Subscription
from django.contrib.auth import authenticate, login
from .serializers import (
    UserRegisterationSerializer,
    UserLoginSerializer,
    PackageSerializer,
    SubscriptionSerializer,
)
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework import filters, permissions


class RegisterViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegisterationSerializer

    @action(detail=False, methods=['POST'], permission_classes=[AllowAny])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(**serializer.validated_data)
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {'token': token.key},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['POST'], permission_classes=[AllowAny])
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return Response(
                    {'message': 'Login successful.'},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'message': 'Login failed. Invalid credentials.'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    filter_backends = (filters.OrderingFilter, filters.SearchFilter)
    ordering_fields = ['price']
    search_fields = ['name']


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def create(self, request, *args, **kwargs):
        package_ids = request.data.get('packages', [])
        user = request.user

        try:
            subscription = Subscription.objects.create(user=user)
            subscription.packages.set(package_ids)

            return Response(
                SubscriptionSerializer(subscription).data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class UserSubscriptionsViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)
