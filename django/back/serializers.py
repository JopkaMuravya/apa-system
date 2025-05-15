from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'email', 'first_name', 'last_name', 'middle_name',
            'password', 'role', 'is_superuser', 'full_name',
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def get_full_name(self, obj):
        parts = filter(None, [obj.last_name, obj.first_name, obj.middle_name])
        return ' '.join(parts)

    def create(self, validated_data):
        return User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            middle_name=validated_data.get('middle_name', ''),
            role='waiting',
        )