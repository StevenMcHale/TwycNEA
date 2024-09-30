from django.urls import path
from . import views

urlpatterns = [
    path('registerStudent/', views.registerStudentPage, name="registerStudent"),
    path('registerTeacher/', views.registerTeacherPage, name="registerTeacher"),
    path('registerParent/', views.registerParentPage, name="registerParent"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    path('userStudent/', views.userStudent, name="userStudent"),
    path('userTeacher/', views.userTeacher, name="userTeacher"),
    path('userParent/', views.userParent, name="userParent"),

    path('userStudentBookings/', views.userStudentBookings, name="userStudentBookings"),
    path('userTeacherBookings/', views.userTeacherBookings, name="userTeacherBookings"),
]