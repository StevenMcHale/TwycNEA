from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('bookings/', views.bookings, name="bookings"),
    path('student/<str:pk>/', views.student, name="student"),
    path('teacher/<str:pk>/', views.teacher, name="teacher"),
    path('room/<str:pk>/', views.room, name="room"),
    path('building/<str:pk>/', views.building, name="building"),
    path('subject/<str:pk>/', views.subject, name="subject"),
    path('date/<str:pk>/', views.date, name="date"),
    path('timeslot/<str:pk>/', views.timeslot, name="timeslot"),
    path('sheetLVI/', views.spreadsheetLVI, name="sheetLVI"),
    path('sheetUVI/', views.spreadsheetUVI, name="sheetUVI"),
    path('parent/<str:pk>/', views.parent, name="parent"),
    path('map/', views.map, name="map"),
]
