

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.views.generic import *
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from app.forms import AsistenciaForm
from app.models import Miembro, Asistencia
from django.views.decorators.csrf import csrf_exempt


class RegistrarAsistenciaView(CreateView):
    template_name = 'asistencia/asistencia.html'
    form_class = AsistenciaForm
    success_url = reverse_lazy('asys:miembro_list')
    reverse_lazy = reverse_lazy('asys:miembro_list')
    url_redirect = success_url

    # def post(self, request, *args, **kwargs):
    #     data = {}
    #     try:
    #         action = request.POST['action']
    #         if action == 'searchdata':
    #             data = []
    #             for i in Miembro.objects.all():
    #                 data.append(i.toJSON())
    #         else:
    #             data['error'] = 'Ha ocurrido un error'
    #     except Exception as e:
    #         data['error'] = str(e)
    #     return JsonResponse(data, safe=False)

    def form_valid(self, form):
        fecha = form.cleaned_data['fecha']
        estado = form.cleaned_data['estado']
        usuarios = form.cleaned_data['usuarios']

        for miembro in usuarios:
            asistencia = Asistencia(
                usuario=miembro,
                fecha=fecha,
                estado=estado,
                status=True if estado == 'Presente' else False
            )
            asistencia.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Asistencia'
        context['entity'] = 'Asistencia'
        context['list_url'] = self.success_url
        context['action'] = 'add'

        miembros = Miembro.objects.all()
        paginator = Paginator(miembros, 90)  # Dividir en páginas de 6 miembros cada una
        page_number = self.request.GET.get('page')

        try:
            miembros_pagina = paginator.page(page_number)
        except PageNotAnInteger:
            miembros_pagina = paginator.page(1)
        except EmptyPage:
            miembros_pagina = paginator.page(paginator.num_pages)

        context['miembros'] = miembros_pagina

        return context


class AsistenciaListView(ListView):
    model = Asistencia
    template_name = 'asistencia/list.html'


    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Miembro.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Asistencia'
        context['create_url'] = reverse_lazy('asys:members_create')
        context['list_url'] = reverse_lazy('miembro_list')
        context['entity'] = 'Miembros'
        return context
