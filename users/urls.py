from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import CustomUserCreate, BlacklistTokenUpdateView, UserInformationView, UserFavoriesNoodlesView, addToFavorites, create_payment, OrderView, GetUserOrders, UserSingleOrder

app_name = 'users'

urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('create-payment-intent', create_payment.as_view()),
    path('create-order/<str:user_name>', OrderView.as_view()),
    path('user-orders/<str:user_name>', GetUserOrders.as_view()),
    path('user-order/<str:user_name>/<int:order_id>', UserSingleOrder.as_view()),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('user-details/<int:pk>', UserInformationView.as_view(), name='user-details'),
    path('user-favorites/<str:user_name>/<str:slug>/',
         addToFavorites.as_view(), name='user-favorites'),
    path('user-favories-noodles/<int:pk>',
         UserFavoriesNoodlesView.as_view(), name='user-favories-noodles'),

    path('create/', CustomUserCreate.as_view(), name="create_user"),
    path('logout/blacklist/', BlacklistTokenUpdateView.as_view(),
         name='blacklist')
]
