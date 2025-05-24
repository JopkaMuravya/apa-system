from django.urls import path
from .views import (
    RegisterAPI,
    LoginAPI,
    UserListAPI,
    GroupListAPI,
    GroupDetailAPI,
    CurrentUserAPI,
    TeacherSubjectsAPI,
)

urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/users/', UserListAPI.as_view(), name='user-list'),
    path('api/groups/', GroupListAPI.as_view(), name='group-list'),
    path('api/groups/<int:pk>/', GroupDetailAPI.as_view(), name='group-detail'),
    path('api/users/<int:pk>/', UserListAPI.as_view(), name='user-detail'),
    path('api/current-user/', CurrentUserAPI.as_view(), name='current-user'),
    path('api/teacher/subjects/', TeacherSubjectsAPI.as_view(), name='teacher-subjects'),
]
