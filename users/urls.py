from django.urls import path
from .views import CustomUserCreate, BlacklistTokenUpdateView, UserInformation

app_name = 'users'

urlpatterns = [
    path('user-details/<int:pk>', UserInformation.as_view(), name='user-details'),

    path('create/', CustomUserCreate.as_view(), name="create_user"),
    path('logout/blacklist/', BlacklistTokenUpdateView.as_view(),
         name='blacklist')
]
