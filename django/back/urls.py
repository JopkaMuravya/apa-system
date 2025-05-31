from django.urls import path
from .views import (
    RegisterAPI,
    LoginAPI,
    UserListAPI,
    GroupListAPI,
    GroupDetailAPI,
<<<<<<< HEAD
    CurrentUserAPI,
    TeacherSubjectsAPI,
=======
    GroupSubjectTeacherAPI,
    SubjectListWithTeachersAPI,  
>>>>>>> origin/Nania
)

urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/users/', UserListAPI.as_view(), name='user-list'),
    path('api/users/<int:pk>/', UserListAPI.as_view(), name='user-detail'),
    path('api/groups/', GroupListAPI.as_view(), name='group-list'),
    path('api/groups/<int:pk>/', GroupDetailAPI.as_view(), name='group-detail'),
<<<<<<< HEAD
    path('api/users/<int:pk>/', UserListAPI.as_view(), name='user-detail'),
    path('api/current-user/', CurrentUserAPI.as_view(), name='current-user'),
    path('api/teacher/subjects/', TeacherSubjectsAPI.as_view(), name='teacher-subjects'),
=======
    path('api/groups/<int:group_id>/subject_teachers/', GroupSubjectTeacherAPI.as_view(), name='group-subject-teacher'),
    path('api/subjects/', SubjectListWithTeachersAPI.as_view(), name='subject-list-with-teachers'),
>>>>>>> origin/Nania
]
