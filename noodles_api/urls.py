from django.contrib import admin
from django.urls import path, include
from api.views import Home

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home.as_view(), name='home'),  # Homepage
    path('api/v1/', include('api.urls')),  # api/v1/noodles/
    path('api/users/', include('users.urls', namespace='users')),  # users.urls.py

    # path('api/v1/', include('djoser.urls')),
    # path('api/v1/', include('djoser.urls.authtoken')),
    # path('api/v1/', include('djoser.urls')),


    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# handler404 = "django_404_project.views.page_not_found_view"
