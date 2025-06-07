from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, get_user_model

from .models import Group, Subject, StudentGroup, TeacherSubject, GroupSubjectTeacher, Grade, TeacherComment
from .serializers import UserSerializer, GroupSerializer, GroupDetailSerializer, SubjectSerializer, \
    GroupSubjectTeacherSerializer, TeacherCommentSerializer, GradeAssignmentSerializer
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

    def delete(self, request, pk=None):
        try:
            subject = Subject.objects.get(pk=pk)
            subject.delete()
            return Response({'success': True}, status=status.HTTP_204_NO_CONTENT)
        except Subject.DoesNotExist:
            return Response({'detail': 'Предмет не найден'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk=None):
        name = request.data.get('name', '').strip()
        teacher_ids = request.data.get('teacher_ids', [])

        if not name:
            return Response({'detail': 'Название предмета обязательно'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            subject = Subject.objects.get(pk=pk)
        except Subject.DoesNotExist:
            return Response({'detail': 'Предмет не найден'}, status=status.HTTP_404_NOT_FOUND)

        if Subject.objects.exclude(pk=pk).filter(name__iexact=name).exists():
            return Response({'detail': 'Предмет с таким названием уже существует'}, status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(teacher_ids, list):
            return Response({'detail': 'teacher_ids должен быть списком'}, status=status.HTTP_400_BAD_REQUEST)

        subject.name = name
        subject.save()

        from .models import TeacherSubject
        TeacherSubject.objects.filter(subject=subject).delete()

        teachers = User.objects.filter(id__in=teacher_ids, role='teacher')
        for teacher in teachers:
            TeacherSubject.objects.create(subject=subject, teacher=teacher)

        return Response({'success': True}, status=status.HTTP_200_OK)


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

    def put(self, request, group_id):
        subject_id = request.data.get('subject_id')
        teacher_id = request.data.get('teacher_id')

        if not subject_id or not teacher_id:
            return Response({'detail': 'subject_id и teacher_id обязательны'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            assignment = GroupSubjectTeacher.objects.get(group_id=group_id, subject_id=subject_id)
        except GroupSubjectTeacher.DoesNotExist:
            return Response({'detail': 'Назначение не найдено'}, status=status.HTTP_404_NOT_FOUND)

        try:
            teacher = User.objects.get(id=teacher_id, role='teacher')
        except User.DoesNotExist:
            return Response({'detail': 'Преподаватель не найден'}, status=status.HTTP_404_NOT_FOUND)

        assignment.teacher = teacher
        assignment.save()

        return Response({'success': True}, status=status.HTTP_200_OK)

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


class SubjectCreateWithTeachersAPI(APIView):
    permission_classes = [IsModerator]

    def post(self, request):
        name = request.data.get('name')
        teacher_ids = request.data.get('teacher_ids', [])

        if not name or not name.strip():
            return Response({'detail': 'Название предмета обязательно'}, status=status.HTTP_400_BAD_REQUEST)

        if Subject.objects.filter(name__iexact=name.strip()).exists():
            return Response({'detail': 'Предмет с таким названием уже существует'}, status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(teacher_ids, list):
            return Response({'detail': 'teacher_ids должен быть списком'}, status=status.HTTP_400_BAD_REQUEST)

        subject = Subject.objects.create(name=name.strip())

        teachers = User.objects.filter(id__in=teacher_ids, role='teacher')
        for teacher in teachers:
            from .models import TeacherSubject
            TeacherSubject.objects.create(subject=subject, teacher=teacher)

        return Response({'success': True, 'subject_id': subject.id}, status=status.HTTP_201_CREATED)


class CurrentUserAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        data = serializer.data
        if request.user.role == 'student':
            student_group = StudentGroup.objects.filter(student=request.user).select_related('group').first()
            if student_group:
                data['group'] = {
                    'id': student_group.group.id,
                    'name': student_group.group.name
                }
            else:
                data['group'] = None
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


class TeacherGroupsAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, subject_id=None):
        try:
            if request.user.role != 'teacher':
                return Response({'detail': 'Доступ запрещен'}, status=403)

            groups = Group.objects.filter(
                teaching_assignments__teacher=request.user,
                teaching_assignments__subject_id=subject_id
            ).distinct()

            serializer = GroupSerializer(groups, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'detail': str(e)}, status=500)


class StudentSubjectsAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            if request.user.role != 'student':
                return Response({'detail': 'Доступ запрещен'}, status=403)

            student_groups = StudentGroup.objects.filter(student=request.user).values_list('group', flat=True)
            subjects = Subject.objects.filter(group_teaching_assignments__group__in=student_groups).distinct()

            serializer = SubjectSerializer(subjects, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'detail': str(e)}, status=500)


class GradeAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, group_id, subject_id):
        if request.user.role != 'teacher':
            return Response({'detail': 'Доступ запрещен'}, status=403)

        try:
            group = Group.objects.get(id=group_id)
            subject = Subject.objects.get(id=subject_id)

            # Проверяем, что преподаватель ведет этот предмет в группе
            if not GroupSubjectTeacher.objects.filter(
                    group=group,
                    subject=subject,
                    teacher=request.user
            ).exists():
                return Response({'detail': 'Преподаватель не ведет этот предмет в группе'}, status=403)

            # Получаем всех студентов группы
            students = User.objects.filter(
                student_groups__group=group,
                role='student'
            ).distinct()

            # Получаем все задания по предмету
            assignments = Grade.objects.filter(
                group=group,
                subject=subject
            ).values_list('assignment_name', flat=True).distinct()

            # Получаем комментарий преподавателя
            teacher_comment = TeacherComment.objects.filter(
                teacher=request.user,
                group=group,
                subject=subject
            ).first()

            # Формируем данные для таблицы
            grades_data = []
            for student in students:
                student_grades = {'student': student.id, 'full_name': f"{student.last_name} {student.first_name}"}
                for assignment in assignments:
                    try:
                        grade = Grade.objects.get(
                            student=student,
                            group=group,
                            subject=subject,
                            assignment_name=assignment
                        )
                        student_grades[assignment] = grade.value
                    except Grade.DoesNotExist:
                        student_grades[assignment] = ''
                grades_data.append(student_grades)

            return Response({
                'assignments': list(assignments),
                'grades': grades_data,
                'comment': teacher_comment.comment if teacher_comment else '',
                'link': teacher_comment.link if teacher_comment else ''
            })
        except Exception as e:
            return Response({'detail': str(e)}, status=500)

    def post(self, request, group_id, subject_id):
        serializer = GradeAssignmentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        try:
            group = Group.objects.get(id=group_id)
            subject = Subject.objects.get(id=subject_id)
            assignment_name = serializer.validated_data['assignment_name']

            # Создаем/обновляем оценки
            for student_id, grade_value in serializer.validated_data['grades'].items():
                student = User.objects.get(id=student_id, role='student')
                Grade.objects.update_or_create(
                    student=student,
                    group=group,
                    subject=subject,
                    assignment_name=assignment_name,
                    defaults={'value': grade_value}
                )

            return Response({'success': True})
        except Exception as e:
            return Response({'detail': str(e)}, status=500)

    def put(self, request, group_id, subject_id):
        serializer = TeacherCommentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        try:
            group = Group.objects.get(id=group_id)
            subject = Subject.objects.get(id=subject_id)

            # Создаем или обновляем комментарий преподавателя
            teacher_comment, created = TeacherComment.objects.update_or_create(
                teacher=request.user,
                group=group,
                subject=subject,
                defaults={
                    'comment': serializer.validated_data['comment'],
                    'link': serializer.validated_data['link']
                }
            )

            return Response({
                'success': True,
                'comment': teacher_comment.comment,
                'link': teacher_comment.link
            })
        except Exception as e:
            return Response({'detail': str(e)}, status=500)