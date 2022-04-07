from django.urls import path
from .views import CustomUserCreate, BlacklistTokenUpdateView, UserInformationView, UserFavoriesNoodlesView, addToFavorites

app_name = 'users'

urlpatterns = [
    path('user-details/<int:pk>', UserInformationView.as_view(), name='user-details'),
    path('user-favorites/<str:user_name>/<str:slug>/',
         addToFavorites.as_view(), name='user-favorites'),
    path('user-favories-noodles/<int:pk>',
         UserFavoriesNoodlesView.as_view(), name='user-favories-noodles'),

    path('create/', CustomUserCreate.as_view(), name="create_user"),
    path('logout/blacklist/', BlacklistTokenUpdateView.as_view(),
         name='blacklist')
]
