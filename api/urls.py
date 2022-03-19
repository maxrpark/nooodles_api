from django.urls import path

from . import views

urlpatterns = [
    path('noodles/', views.NoodlesView.as_view(), name='noodles'),
]
