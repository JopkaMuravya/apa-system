from rest_framework import serializers
from .models import User, Group, Subject, GroupSubjectTeacher, Grade, TeacherComment


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    full_name = serializers.SerializerMethodField()
    group_name = serializers.SerializerMethodField() 
    email = serializers.EmailField(required=True)

    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = (
            'id', 'email', 'first_name', 'last_name', 'middle_name',
            'password', 'role', 'is_superuser', 'full_name', 'group_name',
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def get_full_name(self, obj):
        parts = filter(None, [obj.last_name, obj.first_name, obj.middle_name])
        return ' '.join(parts)

    def get_group_name(self, obj): 
        group_relation = obj.student_groups.first()
        return group_relation.group.name if group_relation else None

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
            raise serializers.ValidationError("Пользователь с такой почтой уже существует")
        return value

    def validate(self, data):
        first_name = data.get('first_name', '').strip()
        last_name = data.get('last_name', '').strip()

        if not first_name or not last_name or not first_name.isalpha() or not last_name.isalpha():
            raise serializers.ValidationError("Введите корректное ФИО")

        return data


from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Group

class GroupSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=100,
        validators=[
            UniqueValidator(
                queryset=Group.objects.all(),
                message='Группа с таким названием уже существует.'
            )
        ]
    )

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
        links = GroupSubjectTeacher.objects.filter(group=group).select_related('subject', 'teacher')
        return [
            {
                'id': link.subject.id,
                'name': link.subject.name,
                'teacher': f"{link.teacher.last_name} {link.teacher.first_name} {link.teacher.middle_name or ''}".strip()
            }
            for link in links
        ]

    def get_students(self, group):
        return [
            {
                'id': student.id,
                'full_name': f"{student.last_name} {student.first_name} {student.middle_name or ''}".strip(),
                'email': student.email
            }
            for student in User.objects.filter(student_groups__group=group)
        ]


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name']

        
class GroupSubjectTeacherSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(source='group.name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    teacher_name = serializers.SerializerMethodField()

    class Meta:
        model = GroupSubjectTeacher
        fields = ['id', 'group', 'group_name', 'subject', 'subject_name', 'teacher', 'teacher_name']

    def get_teacher_name(self, obj):
        return f"{obj.teacher.last_name} {obj.teacher.first_name} {obj.teacher.middle_name or ''}".strip()


class SubjectWithTeachersSerializer(serializers.ModelSerializer):
    teachers = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = ['id', 'name', 'teachers']

    def get_teachers(self, subject):
        links = subject.subject_teachers.select_related('teacher')
        return [
            {
                'id': link.teacher.id,
                'full_name': f"{link.teacher.last_name} {link.teacher.first_name} {link.teacher.middle_name or ''}".strip()
            }
            for link in links
        ]


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ['id', 'student', 'subject', 'group', 'assignment_name', 'value']
        read_only_fields = ['id']


class GradeAssignmentSerializer(serializers.Serializer):
    assignment_name = serializers.CharField(max_length=255)
    grades = serializers.DictField(child=serializers.CharField(max_length=10))


class TeacherCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherComment
        fields = ['comment', 'link']
