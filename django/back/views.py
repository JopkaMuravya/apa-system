from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, get_user_model

from .models import Group, GroupSubject, StudentGroup, TeacherSubject, Subject
from .serializers import UserSerializer, GroupSerializer, GroupDetailSerializer, SubjectSerializer
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


class CurrentUserAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Проверка роли пользователя
        if request.user.role != 'student':
            return Response({'detail': 'Доступ запрещен'}, status=403)

        serializer = UserSerializer(request.user)
        data = serializer.data
        # Получаем группу студента
        student_group = StudentGroup.objects.filter(student=request.user).select_related('group').first()
        if student_group:
            data['group'] = {
                'id': student_group.group.id,
                'name': student_group.group.name
            }
        else:
            data['group'] = None
        return Response(data)



class TeacherSubjectsAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        teacher_subjects = TeacherSubject.objects.filter(teacher=request.user).select_related('subject')
        subjects = [ts.subject for ts in teacher_subjects]

        serializer = SubjectSerializer(subjects, many=True)

        return Response(serializer.data)
class StudentSubjectsAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Получаем группу, в которых состоит студент
        student_groups = StudentGroup.objects.filter(student=request.user).values_list('group', flat=True)
        # Получаем предметы, связанные с этими группами
        subjects = Subject.objects.filter(subject_groups__group__in=student_groups).distinct()

        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data)