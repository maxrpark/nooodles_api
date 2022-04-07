from django.views import View
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomUserSerializer, UserDetailsSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny

from .models import NewUser as Users
from api.models import Noodle
from api.utils import noodleList


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
                {"error": "email_exist",
                 "messege": "This email address is already used by another account."}, status=status.HTTP_400_BAD_REQUEST)

        if(request.data['email'].find('@') == -1 or request.data['email'].find('.') == -1):
            return Response(
                {"error": "email_error",
                 "message": "Please enter a valid email address"},
                status=status.HTTP_400_BAD_REQUEST)

        if len(request.data['user_name']) < 3:
            return Response(
                {"error": "user_name_length",
                 "messege": "User name must be at least 3 characters long."},
                status=status.HTTP_400_BAD_REQUEST)

        if all_users.filter(user_name=request.data['user_name']).exists():
            return Response(
                {"error": "user_name_exist",
                 "messege": "User name already exists, please choose another one."}, status=status.HTTP_400_BAD_REQUEST)

        if len(request.data['password']) < 8:
            return Response(
                {"error": "password_length",
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


class UserInformationView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()

    def get(self, request, pk):
        try:
            user = Users.objects.get(pk=pk)
            serializer = UserDetailsSerializer(user)
            return Response(serializer.data)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserFavoriesNoodlesView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()

    def get(self, request, pk):
        try:
            user = Users.objects.get(pk=pk)
            user_favories = user.favorites.all()
            if(user_favories.count() > 0):
                return noodleList(user_favories)
            else:
                return JsonResponse({'error': 'No favorites on your list'}, safe=False)
        except Exception as e:
            return JsonResponse({'error': 'No User'}, status=status.HTTP_400_BAD_REQUEST)


class addToFavorites(APIView):
    # permission_classes = [AllowAny]
    # authentication_classes = ()

    def post(self, request, user_name, slug):
        try:
            user = Users.objects.get(user_name=user_name)
            noodle = Noodle.objects.get(slug=slug)
            if user.favorites.filter(slug=noodle.slug).exists():
                user.favorites.remove(noodle)
            else:
                user.favorites.add(noodle)
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
