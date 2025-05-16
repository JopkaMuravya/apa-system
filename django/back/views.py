from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, get_user_model

from .models import Group
from .serializers import UserSerializer, GroupSerializer
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
        user_id = request.data.get('id')
        new_role = request.data.get('role')

        try:
            user = User.objects.get(id=user_id)
            user.role = new_role
            user.save()
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
