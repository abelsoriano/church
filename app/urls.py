from django.urls import path

from app.views.asistencia.views import *
from app.views.persona.views import *
from app.views.servicio.views import ServicioCreateView

# from app.views.persona.views import


app_name = 'asys'

urlpatterns = [
    path('persona/list/', MembersListView.as_view(), name='miembro_list'),
    path('persona/add/', MembersCreate.as_view(), name='members_create'),
    path('persona/edit/<int:pk>/', MembersUpdate.as_view(), name='members_update'),
    path('persona/delete/<int:pk>/', MembersDelete.as_view(), name='members_delete'),

    path('servicio/create/', login_required(ServicioCreateView.as_view()), name='servicio_create'),


    path('crear-asistencia/', AttendanceCreateView.as_view(), name='crear_asistencia'),
    path('lista-asistencia/', AttendanceList.as_view(), name='list_asistencia'),
    path('details/', AttendanceDetailsView.as_view(), name='details_asistencia'),
# urls.py
#     path('attendance/json/<str:date>/', AttendanceJsonDetail.as_view(), name='attendance_json'),
#     path('lista-asistencia2/', AsistenciaDataTable.as_view(), name='list_asistencia2'),

]

