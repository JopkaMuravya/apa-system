from rest_framework import serializers
from .models import User, Group, Subject, StudentGroup


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    full_name = serializers.SerializerMethodField()
    email = serializers.EmailField(required=True)

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

    def validate_email(self, value):
        request = self.context.get('request')
        current_user_id = None

        if request and request.method == 'PUT':
            current_user_id = request.data.get('id')

        if User.objects.exclude(id=current_user_id).filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с такой почтой уже существует.")
        return value

    def validate(self, attrs):
        if not attrs.get('first_name') or not attrs.get('last_name'):
            raise serializers.ValidationError("Фамилия и имя обязательны для заполнения.")
        return attrs


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


class GroupDetailSerializer(serializers.ModelSerializer):
    subjects = serializers.SerializerMethodField()
    students = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ['id', 'name', 'subjects', 'students']

    def get_subjects(self, group):
        return [{'id': s.id, 'name': s.name} for s in Subject.objects.filter(subject_groups__group=group)]

    def get_students(self, group):
        return [
            {
                'id': student.id,
                'full_name': f"{student.last_name} {student.first_name} {student.middle_name or ''}".strip(),
                'email': student.email
            }
            for student in User.objects.filter(student_groups__group=group)
        ]
