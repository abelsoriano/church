from datetime import date, timedelta
from django.contrib import messages

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count, Q
from django.db.models.functions import  Trunc, Concat, ExtractWeekDay

from django.http import HttpResponseBadRequest, JsonResponse
from django.db.models import Value, CharField

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy

from django.views.generic import *
from django.shortcuts import redirect, get_object_or_404
from app.forms import AsistenciaForm
from app.models import *


class AttendanceCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Attendance
    form_class = AsistenciaForm
    template_name = 'asistencia/AsistenciaCreate.html'
    success_url = reverse_lazy('asys:list_asistencia')

    def post(self, request, *args, **kwargs):
        try:
            miembros = Miembro.objects.filter(category='joven')
            miembros_con_inasistencias = Attendance.objects.filter(miembro__category='joven', present=False).values('miembro').annotate(total_inasistencias=Count('id'))
            miembros_ids_con_inasistencias = [miembro['miembro'] for miembro in miembros_con_inasistencias if miembro['total_inasistencias'] >= 1]

            for miembro in miembros:
                try:
                    present = request.POST.get(f'presente_{miembro.id}', 'False')
                    present = True if present == 'True' else False
                    attendance = Attendance.objects.create(miembro=miembro, present=present, date=timezone.now())
                    if attendance:  # Si la asistencia se creó correctamente
                        if not present and miembro.id in miembros_ids_con_inasistencias:
                            miembro_obj = Miembro.objects.get(id=miembro.id)
                            inasistencias = Attendance.objects.filter(miembro=miembro_obj, present=False).count()
                            messages.warning(request, f"El miembro {miembro_obj.name} {miembro_obj.lastname} ha alcanzado {inasistencias} inasistencias.", extra_tags={'modal_trigger': True, 'miembro_id': miembro_obj.id})
                except Exception as e:
                    messages.error(request, f"Ha ocurrido un error al registrar la asistencia para el miembro {miembro.name}. Error: {str(e)}")

            return redirect('asys:list_asistencia')
        except Exception as e:
            messages.error(request, f"Ha ocurrido un error al registrar la asistencia. Error: {str(e)}")
            return redirect('asys:create_asistencia')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['miembros'] = Miembro.objects.filter(category='joven')
        context['entity'] = 'Attendance'
        context['title'] = 'Creando nueva Asistencia'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

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

def guardar_status(request):
    if request.method == 'POST':
        miembro_id = request.POST.get('miembro_id')
        status = request.POST.get('status')

        if miembro_id and status:
            if miembro_id.isdigit():
                try:
                    miembro = get_object_or_404(Miembro, id=miembro_id)
                    MiembroStatus.objects.create(miembro=miembro, status=status)
                    return redirect('asys:list_asistencia')
                except Miembro.DoesNotExist:
                    messages.error(request, 'El ID del miembro no existe')
            else:
                messages.error(request, 'El ID del miembro no es un número entero')
            return redirect('asys:list_asistencia')
    return redirect('asys:list_asistencia')



class AttendanceList(ListView):
    model = Attendance
    template_name = 'asistencia/AsistenciaList.html'
    context_object_name = 'asistencias'

    def get_inattendance_count(self):
        current_month = date.today().month
        current_year = date.today().year
        month_start = date(current_year, current_month, 1)
        month_end = month_start + timedelta(days=31 - month_start.day)

        # Get all attendances for the current month
        user_attendances = Attendance.objects.filter(
            date__gte=month_start,
            date__lte=month_end
        )
        inattendance_count = user_attendances.filter(present=False).count()
        return inattendance_count

    def get_queryset(self):
        queryset = Attendance.objects.annotate(
            fecha=Trunc('date', 'day'),
            weekday_name=ExtractWeekDay('date')  # Function for day name
        ).values('fecha', 'weekday_name').annotate(
            total=Count('id'),
            total_true=Count('id', filter=Q(present=True)),
            total_false=Count('id', filter=Q(present=False)),
        ).order_by('-fecha')

        # Convert day number to name with list comprehension
        weekdays_mapping = {
            0: 'Domingo',
            1: 'Lunes',
            2: 'Martes',
            3: 'Miércoles',
            4: 'Jueves',
            5: 'Viernes',
            6: 'Sábado'
        }

        for entry in queryset:
            entry['weekday_name'] = weekdays_mapping.get(entry['weekday_name'], 'Desconocido')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Miembros'
        context['create_url'] = reverse_lazy('asys:crear_asistencia')
        context['list_url'] = reverse_lazy('list_asistencia')
        context['entity'] = 'Miembros'
        # inattendance_count = self.get_inattendance_count()  # Get the count value directly
        # context['show_modal'] = inattendance_count >= 2
        return context



class AttendanceDetailsView(View):
    def get(self, request):
        date_str = request.GET.get('date')

        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Formato de fecha inválido. Debe ser YYYY-MM-DD.'}, status=400)

        details = list(Attendance.objects.filter(date=date).annotate(
            miembro_nombre_completo=Concat('miembro__name', Value(' '), 'miembro__lastname', output_field=CharField())
        ).values('id', 'miembro_nombre_completo', 'date', 'present'))

        return JsonResponse({'details': details})


