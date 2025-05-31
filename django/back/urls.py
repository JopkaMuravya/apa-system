from django.urls import path
from .views import (
    RegisterAPI,
    LoginAPI,
    UserListAPI,
    GroupListAPI,
    GroupDetailAPI,
    GroupSubjectTeacherAPI,
    SubjectListWithTeachersAPI,
    SubjectCreateWithTeachersAPI,  
)

urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/users/', UserListAPI.as_view(), name='user-list'),
    path('api/users/<int:pk>/', UserListAPI.as_view(), name='user-detail'),
    path('api/groups/', GroupListAPI.as_view(), name='group-list'),
    path('api/groups/<int:pk>/', GroupDetailAPI.as_view(), name='group-detail'),
    path('api/groups/<int:group_id>/subject_teachers/', GroupSubjectTeacherAPI.as_view(), name='group-subject-teacher'),
    path('api/subjects/', SubjectListWithTeachersAPI.as_view(), name='subject-list-with-teachers'),
    path('api/subjects/create_with_teachers/', SubjectCreateWithTeachersAPI.as_view(), name='subject-create-with-teachers'),
    path('api/subjects/<int:pk>/', SubjectListWithTeachersAPI.as_view()),
]
