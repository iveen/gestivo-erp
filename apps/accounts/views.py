from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from apps.tenants.models import Tenant
from apps.accounts.models import User, Company, Role, UserCompanyRole
from apps.accounts.serializers import (
    TenantSerializer, CompanySerializer, RoleSerializer,
    UserSerializer, UserCompanyRoleSerializer
)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email']     = user.email
        token['full_name'] = user.full_name
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = {
            'id':       str(self.user.id),
            'email':    self.user.email,
            'full_name': self.user.full_name,
        }
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class TenantViewSet(viewsets.ModelViewSet):
    serializer_class   = TenantSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Tenant.objects.all().order_by('name')


class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = CompanySerializer

    def get_queryset(self):
        return Company.objects.all().order_by('name')

    def perform_create(self, serializer):
        serializer.save()


class RoleViewSet(viewsets.ModelViewSet):
    serializer_class = RoleSerializer

    def get_queryset(self):
        return Role.objects.all().order_by('name')

    def perform_create(self, serializer):
        serializer.save()


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all().order_by('email')

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class UserCompanyRoleViewSet(viewsets.ModelViewSet):
    serializer_class = UserCompanyRoleSerializer

    def get_queryset(self):
        return UserCompanyRole.objects.all().select_related('user', 'company', 'role')

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.tenant)