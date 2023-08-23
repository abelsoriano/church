from django.urls import path

from app.views.asistencia.views import *
from app.views.persona.views import *
# from app.views.persona.views import list_miembro


app_name = 'asys'

urlpatterns = [
    path('persona/list/', MembersListView.as_view(), name='miembro_list'),
    path('persona/add/', MembersCreate.as_view(), name='members_create'),
    path('persona/edit/<int:pk>/', MembersUpdate.as_view(), name='members_update'),
    path('persona/delete/<int:pk>/', MembersDelete.as_view(), name='members_delete'),
    path('registro/', RegistrarAsistenciaView.as_view(), name='registrar'),
    path('asistencia/list/', AsistenciaListView.as_view(), name='asistencia_list'),
   # path('asistencias/', RegistrarAsistenciaView.as_view(), name='asistencias'),

 # path('reporte/', ReporteAsistenciaView.as_view(), name='reporte'),
]
    # path('persona/delete/<int:pk>/', MembersDelete.as_view(), name='members_delete'),
    # path('persona/list2/', list_miembro, name='list_miembro')
    # path('', index, name="index")

