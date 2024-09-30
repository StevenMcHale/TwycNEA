from django.urls import path
from . import views

urlpatterns = [
    path('delete_all_uvi/', views.deleteAll, name="delete_all_uvi"),
    path('convert_all_lvi/', views.convertAll, name="convert_all_lvi"),

    path('create_parent/', views.createParent, name="create_parent"),
    path('edit_parent/<str:pk>/', views.editParent, name="edit_parent"),
    path('delete_parent/<str:pk>/', views.deleteParent, name="delete_parent"),

    path('create_building/', views.createBuilding, name="create_building"),
    path('edit_building/<str:pk>/', views.editBuilding, name="edit_building"),
    path('delete_building/<str:pk>/', views.deleteBuilding, name="delete_building"),

    path('create_room/', views.createRoom, name="create_room"),
    path('edit_room/<str:pk>/', views.editRoom, name="edit_room"),
    path('delete_room/<str:pk>/', views.deleteRoom, name="delete_room"),

    path('create_subject/', views.createSubject, name="create_subject"),
    path('edit_subject/<str:pk>/', views.editSubject, name="edit_subject"),
    path('delete_subject/<str:pk>/', views.deleteSubject, name="delete_subject"),

    path('create_timeslot/', views.createTimeslot, name="create_timeslot"),
    path('edit_timeslot/<str:pk>/', views.editTimeslot, name="edit_timeslot"),
    path('delete_timeslot/<str:pk>/', views.deleteTimeslot, name="delete_timeslot"),

    path('create_eveningDate/', views.createEveningDate, name="create_eveningDate"),
    path('edit_eveningDate/<str:pk>/', views.editEveningDate, name="edit_eveningDate"),
    path('delete_eveningDate/<str:pk>/', views.deleteEveningDate, name="delete_eveningDate"),

    path('create_teacher/', views.createTeacher, name="create_teacher"),
    path('edit_teacher/<str:pk>/', views.editTeacher, name="edit_teacher"),
    path('delete_teacher/<str:pk>/', views.deleteTeacher, name="delete_teacher"),

    path('create_student/', views.createStudent, name="create_student"),
    path('edit_student/<str:pk>/', views.editStudent, name="edit_student"),
    path('delete_student/<str:pk>/', views.deleteStudent, name="delete_student"),

    path('create_booking/', views.adminCreateBooking, name="create_booking"),
    path('admin_edit_booking/<str:pk>/', views.adminEditBooking, name="admin_edit_booking"),
    path('edit_booking/<str:pk>/', views.editBooking, name="edit_booking"),
    path('delete_booking/<str:pk>/', views.deleteBooking, name="delete_booking"),

]