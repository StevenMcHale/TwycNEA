from django.urls import path
from . import views

urlpatterns = [
    path('automatic/', views.automatic, name="auto"),
]
