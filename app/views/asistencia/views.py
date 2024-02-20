
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count, Q
from django.db.models.functions import TruncDate, Extract, Trunc, Concat
from django.http import HttpResponseBadRequest, JsonResponse
from django.db.models import Value, CharField, F

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from django.views.generic import *
from pip._internal.resolution.resolvelib.provider import V

from app.forms import AsistenciaForm
from app.models import *


class AttendanceCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Attendance
    form_class = AsistenciaForm
    template_name = 'asistencia/AsistenciaCreate.html'
    success_url = reverse_lazy('asys:list_asistencia')
    reverse_lazy = reverse_lazy('asys:members_create')
    url_redirect = success_url

    def post(self, request, *args, **kwargs):
        try:
            miembros = Miembro.objects.filter(category='joven')
            for miembro in miembros:
                present = request.POST.get(f'presente_{miembro.id}', 'False')
                present = True if present == 'True' else False
                Attendance.objects.create(miembro=miembro, present=present, date=timezone.now())

            return redirect('asys:miembro_list')
        except Exception as e:
            return HttpResponseBadRequest()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['miembros'] = Miembro.objects.filter(category='joven')
        context['entity'] = 'Attendance'
        context['title'] = 'Creando nueva Asistencia'
        context['list_url'] = self.success_url
        context['action'] = 'add'

        ################################ paginacion #################################
        miembros = Miembro.objects.filter(category='joven')
        paginator = Paginator(miembros, 90)  # Dividir en páginas de 90 miembros cada una
        page_number = self.request.GET.get('page')
        try:
            miembros_pagina = paginator.page(page_number)
        except PageNotAnInteger:
            miembros_pagina = paginator.page(1)
        except EmptyPage:
            miembros_pagina = paginator.page(paginator.num_pages)
        context['miembros'] = miembros_pagina
        return context


class AttendanceList(ListView):
    model = Attendance
    template_name = 'asistencia/AsistenciaList.html'
    context_object_name = 'asistencias'

    def get_queryset(self):
        queryset = Attendance.objects.annotate(
            fecha=Trunc('date', 'day'),
            weekday_name = Extract('date', 'dow')
        ).values('fecha', 'weekday_name').annotate(
            total=Count('id')
        ).order_by('-fecha')

        # Convierte el número del día de la semana al nombre correspondiente
        weekdays_mapping = {
            0: 'Domingo',
            1: 'Lunes',
            2: 'Martes',
            3: 'Miércoles',
            4: 'Jueves',
            5: 'Viernes',
            6: 'Sábado',
        }

        for entry in queryset:
            entry['weekday_name'] = weekdays_mapping.get(entry['weekday_name'], 'Desconocido')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Miembros'
        context['create_url'] = reverse_lazy('asys:crear_asistencia')
        context['list_url'] = reverse_lazy('miembro_list')
        context['entity'] = 'Miembros'
        return context


class AttendanceDetailsView(View):
    def get(self, request):
        date_str = request.GET.get('date')

        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Formato de fecha inválido. Debe ser YYYY-MM-DD.'}, status=400)

        details = list(Attendance.objects.filter(date=date).annotate(
            miembro_nombre_completo=Concat('miembro__name', Value(' '), 'miembro__lastname', output_field=CharField() )
        ).values('id', 'miembro_nombre_completo', 'date', 'present'))

        return JsonResponse({'details': details})
