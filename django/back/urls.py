from django.urls import path
from .views import RegisterAPI, LoginAPI, UserListAPI, GroupListAPI

urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/users/', UserListAPI.as_view(), name='user-list'),
    path('api/groups/', GroupListAPI.as_view(), name='group-list'),
]