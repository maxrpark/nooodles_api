from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomUserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny

from .models import NewUser as Users


class CustomUserCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format='json'):
        all_users = Users.objects.all()

        if(len(request.data['email']) == 0 or len(request.data['user_name']) == 0 or len(request.data['password']) == 0):
            return Response(
                {"error": "empty_values",
                 "message": "Please fill all the fields"},
                status=status.HTTP_400_BAD_REQUEST)

        if all_users.filter(email=request.data['email']).exists():
            return Response(
                {"error": "email_error",
                 "messege": "This email address is already used by another account."}, status=status.HTTP_400_BAD_REQUEST)

        if(request.data['email'].find('@') == -1 or request.data['email'].find('.') == -1):
            return Response(
                {"error": "email_error",
                 "message": "Please enter a valid email address"},
                status=status.HTTP_400_BAD_REQUEST)

        if len(request.data['user_name']):
            if len(request.data['user_name']) < 3:
                return Response(
                    {"error": "user_name",
                     "messege": "User name must be at least 3 characters long."},
                    status=status.HTTP_400_BAD_REQUEST)

        if all_users.filter(user_name=request.data['user_name']).exists():
            return Response(
                {"error": "user_name_error",
                 "messege": "User name already exists, please choose another one."}, status=status.HTTP_400_BAD_REQUEST)

        if len(request.data['password']):
            if len(request.data['password']) < 8:
                return Response(
                    {"error": "password_error",
                     "messege": "Password must be at least 8 characters long."},
                    status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = CustomUserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                if user:
                    json = serializer.data
                    return Response(json, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlacklistTokenUpdateView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
