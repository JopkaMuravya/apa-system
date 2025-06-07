from django.urls import path
from .views import (
    RegisterAPI,
    LoginAPI,
    UserListAPI,
    GroupListAPI,
    GroupDetailAPI,
    CurrentUserAPI,
    TeacherSubjectsAPI,
    TeacherGroupsAPI,
    StudentSubjectsAPI,
    GroupSubjectTeacherAPI,
    SubjectListWithTeachersAPI,
    SubjectCreateWithTeachersAPI, GradeAPI,
)

urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/users/', UserListAPI.as_view(), name='user-list'),
    path('api/users/<int:pk>/', UserListAPI.as_view(), name='user-detail'),
    path('api/groups/', GroupListAPI.as_view(), name='group-list'),
    path('api/groups/<int:pk>/', GroupDetailAPI.as_view(), name='group-detail'),
    path('api/users/<int:pk>/', UserListAPI.as_view(), name='user-detail'),
    path('api/current-user/', CurrentUserAPI.as_view(), name='current-user'),
    path('api/teacher/subjects/', TeacherSubjectsAPI.as_view(), name='teacher-subjects'),
    path('api/student/subjects/', StudentSubjectsAPI.as_view(), name='student-subjects'),
    path('api/groups/<int:group_id>/subject_teachers/', GroupSubjectTeacherAPI.as_view(), name='group-subject-teacher'),
    path('api/subjects/', SubjectListWithTeachersAPI.as_view(), name='subject-list-with-teachers'),
    path('api/subjects/create_with_teachers/', SubjectCreateWithTeachersAPI.as_view(), name='subject-create-with-teachers'),
    path('api/subjects/<int:pk>/', SubjectListWithTeachersAPI.as_view()),
    path('api/teacher/subjects/<int:subject_id>/groups/', TeacherGroupsAPI.as_view(), name='teacher-subject-groups'),
    path('api/grades/<int:group_id>/<int:subject_id>/', GradeAPI.as_view(), name='grade-api'),
]
