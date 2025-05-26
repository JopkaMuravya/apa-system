from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, get_user_model

from .models import Group, Subject, StudentGroup, GroupSubjectTeacher
from .serializers import UserSerializer, GroupSerializer, GroupDetailSerializer, GroupSubjectTeacherSerializer
from .permissions import IsModerator  

User = get_user_model()


class RegisterAPI(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token.key
        })


class LoginAPI(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "user": UserSerializer(user).data,
                "token": token.key
            })
        return Response({'detail': 'Неверные данные'}, status=status.HTTP_401_UNAUTHORIZED)


class UserListAPI(APIView):
    permission_classes = [IsModerator]

    def get(self, request):
        users = User.objects.exclude(role__in=['moderator', 'admin'])
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def put(self, request):
        try:
            user = User.objects.get(id=request.data.get('id'))
        except User.DoesNotExist:
            return Response({'detail': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data, partial=True, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({'success': True})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk=None):
        try:
            user = User.objects.get(id=pk)
            user.delete()
            return Response({'success': True})
        except User.DoesNotExist:
            return Response({'error': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)


class GroupListAPI(APIView):
    permission_classes = [IsModerator]

    def get(self, request):
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupDetailAPI(APIView):
    permission_classes = [IsModerator]

    def get(self, request, pk):
        try:
            group = Group.objects.get(pk=pk)
        except Group.DoesNotExist:
            return Response({'error': 'Группа не найдена'}, status=status.HTTP_404_NOT_FOUND)

        serializer = GroupDetailSerializer(group)
        return Response(serializer.data)

    def delete(self, request, pk):
        student_id = request.query_params.get('student_id')

        if not student_id:
            return Response({'detail': 'student_id обязателен'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            student_group = StudentGroup.objects.get(group_id=pk, student_id=student_id)
            student_group.delete()
            return Response({'success': True}, status=status.HTTP_204_NO_CONTENT)
        except StudentGroup.DoesNotExist:
            return Response({'detail': 'Такой студент не состоит в группе'}, status=status.HTTP_404_NOT_FOUND)
        
    def post(self, request, pk):
        student_id = request.data.get('student_id')

        if not student_id:
            return Response({'detail': 'student_id обязателен'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            group = Group.objects.get(pk=pk)
            student = User.objects.get(pk=student_id, role='student')
        except Group.DoesNotExist:
            return Response({'detail': 'Группа не найдена'}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({'detail': 'Студент не найден'}, status=status.HTTP_404_NOT_FOUND)

        if StudentGroup.objects.filter(group=group, student=student).exists():
            return Response({'detail': 'Студент уже состоит в этой группе'}, status=status.HTTP_400_BAD_REQUEST)

        StudentGroup.objects.filter(student=student).delete()

        StudentGroup.objects.create(student=student, group=group)

        return Response({'success': True}, status=status.HTTP_201_CREATED)


class SubjectListWithTeachersAPI(APIView):
    permission_classes = [IsModerator]

    def get(self, request):
        subjects = Subject.objects.all().order_by('name')
        from .serializers import SubjectWithTeachersSerializer
        serializer = SubjectWithTeachersSerializer(subjects, many=True)
        return Response(serializer.data)


class GroupSubjectTeacherAPI(APIView):
    permission_classes = [IsModerator]

    def get(self, request, group_id):
        entries = GroupSubjectTeacher.objects.filter(group_id=group_id)
        serializer = GroupSubjectTeacherSerializer(entries, many=True)
        return Response(serializer.data)

    def post(self, request, group_id):
        subject_id = request.data.get('subject_id')
        teacher_id = request.data.get('teacher_id')

        if not subject_id or not teacher_id:
            return Response({'detail': 'subject_id и teacher_id обязательны'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            group = Group.objects.get(id=group_id)
            subject = Subject.objects.get(id=subject_id)
            teacher = User.objects.get(id=teacher_id, role='teacher')
        except Group.DoesNotExist:
            return Response({'detail': 'Группа не найдена'}, status=status.HTTP_404_NOT_FOUND)
        except Subject.DoesNotExist:
            return Response({'detail': 'Предмет не найден'}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({'detail': 'Преподаватель не найден'}, status=status.HTTP_404_NOT_FOUND)

        if GroupSubjectTeacher.objects.filter(group=group, subject=subject).exists():
            return Response({'detail': 'Для этой группы и предмета уже назначен преподаватель'}, status=status.HTTP_400_BAD_REQUEST)

        GroupSubjectTeacher.objects.create(group=group, subject=subject, teacher=teacher)
        return Response({'success': True}, status=status.HTTP_201_CREATED)

    def delete(self, request, group_id):
        subject_id = request.query_params.get('subject_id')

        if not subject_id:
            return Response({'detail': 'subject_id обязателен'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            assignment = GroupSubjectTeacher.objects.get(group_id=group_id, subject_id=subject_id)
            assignment.delete()
            return Response({'success': True}, status=status.HTTP_204_NO_CONTENT)
        except GroupSubjectTeacher.DoesNotExist:
            return Response({'detail': 'Назначение не найдено'}, status=status.HTTP_404_NOT_FOUND)
