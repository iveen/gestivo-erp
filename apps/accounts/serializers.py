from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from apps.accounts.models import User, Company, Role, UserCompanyRole, CompanySettings
from apps.tenants.models import Tenant


class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Tenant
        fields = ['id', 'name', 'slug', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model  = Company
        fields = [
            'id', 'tenant', 'name', 'legal_name',
            'tax_id', 'currency', 'is_active'
        ]
        read_only_fields = ['id']
        extra_kwargs = {'tenant': {'required': False}}


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Role
        fields = ['id', 'company', 'name', 'description']
        read_only_fields = ['id']


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=False,
        validators=[validate_password]
    )
    full_name = serializers.ReadOnlyField()

    class Meta:
        model  = User
        fields = [
            'id', 'email', 'first_name', 'last_name',
            'full_name', 'is_active', 'is_staff', 'password'
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class UserCompanyRoleSerializer(serializers.ModelSerializer):
    user_email    = serializers.ReadOnlyField(source='user.email')
    user_name     = serializers.ReadOnlyField(source='user.full_name')
    role_name     = serializers.ReadOnlyField(source='role.name')
    company_name  = serializers.ReadOnlyField(source='company.name')

    class Meta:
        model  = UserCompanyRole
        fields = [
            'id', 'user', 'user_email', 'user_name',
            'company', 'company_name', 'role', 'role_name', 'tenant'
        ]
        read_only_fields = ['id']

class CompanySettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model  = CompanySettings
        fields = [
            'id', 'company',
            'default_ap_account', 'default_ar_account',
            'default_revenue_account', 'default_expense_account',
            'default_cash_account',
            'default_ap_journal', 'default_ar_journal',
        ]
