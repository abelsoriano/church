from django.urls import path

from app.views.asistencia import views
from app.views.asistencia.views import *
from app.views.persona.views import *
from app.views.servicio.views import ServicioCreateView

# from app.views.persona.views import


app_name = 'asys'

urlpatterns = [
    # path('get_inattendance_count/', views.get_inattendance_count, name='get_inattendance_count'),
    path('persona/list/', MembersListView.as_view(), name='miembro_list'),
    path('persona/add/', MembersCreate.as_view(), name='members_create'),
    path('persona/edit/<int:pk>/', MembersUpdate.as_view(), name='members_update'),
    path('persona/delete/<int:pk>/', MembersDelete.as_view(), name='members_delete'),

    path('servicio/create/', login_required(ServicioCreateView.as_view()), name='servicio_create'),


    path('crear-asistencia/', AttendanceCreateView.as_view(), name='crear_asistencia'),
    path('lista-asistencia/', AttendanceList.as_view(), name='list_asistencia'),
    path('details/', AttendanceDetailsView.as_view(), name='details_asistencia'),
    path('guardar-status/', views.guardar_status, name='guardar_status'),
    # path('get_inattendance_count/', views.get_inattendance_count, name='get_inattendance_count'),
    # path('asistencia/get-inattendance-count/', views.get_inattendance_count, name='get_inattendance_count'),


# urls.py
#     path('attendance/json/<str:date>/', AttendanceJsonDetail.as_view(), name='attendance_json'),
#     path('lista-asistencia2/', AsistenciaDataTable.as_view(), name='list_asistencia2'),

]

