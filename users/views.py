from email import message
import json
from locale import currency
from django.conf import settings
from django.views import View
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomUserSerializer, UserDetailsSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny

from .models import NewUser as Users, Order
from api.models import Noodle
from api.utils import noodleList

import stripe


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


def calculate_order_amount(items, discount):
    try:
        paid_amount = 0
        items_amount = sum(item.get(
            'amount') * item.get('price')for item in items)
        if discount > 0:
            paid_amount = items_amount - (items_amount / discount)
        else:
            paid_amount = items_amount
        return int(paid_amount * 100)
    except Exception as e:
        return paid_amount


stripe.api_key = settings.STRIPE_SECRET_KEY


class create_payment(APIView):

    def post(self, request):
        try:
            intent = stripe.PaymentIntent.create(
                amount=calculate_order_amount(
                    request.data['items'], request.data['discount']),
                currency='usd',
                automatic_payment_methods={
                    'enabled': True,
                },
            )
            return JsonResponse({
                'clientSecret': intent['client_secret']
            })
        except Exception as e:
            return JsonResponse(error=str(e)), 403

# add purchase to user history

# save order to database from Order Model


class OrderView(APIView):
    def post(self, request, user_name):
        print(request.data)
        try:
            user = Users.objects.get(user_name=user_name)
            order = Order(
                user=user,
                first_name=request.data['order_details_data']['first_name'],
                last_name=request.data['order_details_data']['last_name'],
                address=request.data['order_details_data']['address'],
                zipcode=request.data['order_details_data']['zipcode'],
                country=request.data['order_details_data']['country'],
                email=request.data['order_details_data']['email'],
                total_amount_without_discount=request.data['order_details_data']['total_amount_without_discount'],
                discount=request.data['order_details_data']['discount'],
                paid_amount=request.data['order_details_data']['paid_amount'],
                stripe_token=request.data['order_details_data']['stripe_token'],
                cart_items=request.data['items'],
            )
            order.save()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class GetUserOrders(APIView):
    def get(self, request, user_name):
        try:
            user = Users.objects.get(user_name=user_name)
            orders = Order.objects.filter(user=user)
            data = []
            for order in orders:
                order_details = {
                    'id': order.id,
                    'created_at': order.created_at,
                    'total_amount_without_discount': order.total_amount_without_discount,
                    'discount': order.discount,
                    'paid_amount': order.paid_amount,
                    'cart_items': order.cart_items,
                }
                data.append(order_details)

            return JsonResponse(data, safe=False)
        except Exception as e:
            return JsonResponse({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)


class UserSingleOrder(APIView):
    def get(self, request, user_name, order_id):
        try:
            user = Users.objects.get(user_name=user_name)
            order = Order.objects.get(id=order_id, user=user)
            order_details = {
                'id': order.id,
                'created_at': order.created_at,
                'total_amount_without_discount': order.total_amount_without_discount,
                'discount': order.discount,
                'paid_amount': order.paid_amount,
                'cart_items': order.cart_items,
            }
            return JsonResponse(order_details, safe=False)
        except Exception as e:
            return JsonResponse({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
