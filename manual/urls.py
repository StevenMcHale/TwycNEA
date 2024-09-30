from django.urls import path
from . import views

urlpatterns = [
    path('manual/', views.manualType, name="manual"),
    path('studentEditManual/<str:pk>/', views.studentEditManualType, name="student_edit_manual"),
]