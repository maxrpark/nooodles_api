from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api.urls')),
    path('api/v1/', include('api.urls')),
]

# handler404 = "django_404_project.views.page_not_found_view"
