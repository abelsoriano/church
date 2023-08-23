from django.views.generic import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from app.forms import MemberForm
from app.models import Miembro
from django.http import JsonResponse


# class ContactoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Miembro
#         fields = '__all__'


# class ContactoAPIView(APIView):
#     def get(self, request):
#         miembro = Miembro.objects.all()
#         serializer = ContactoSerializer(miembro, many=True)
#         return Response(serializer.data)


class MembersListView(ListView):
    model = Miembro
    template_name = 'persona/list.html'


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
        context['title'] = 'Listado de Miembros'
        context['create_url'] = reverse_lazy('asys:members_create')
        context['list_url'] = reverse_lazy('miembro_list')
        context['entity'] = 'Miembros'
        return context
class MembersCreate(CreateView):
    model = Miembro
    form_class = MemberForm
    template_name = 'persona/create.html'
    success_url = reverse_lazy('asys:miembro_list')
    reverse_lazy = reverse_lazy('asys:members_create')
    url_redirect = success_url

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creando nuevo miembro'
        context['entity'] = 'Miembros'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context
class MembersUpdate(UpdateView):
    model = Miembro
    form_class = MemberForm
    template_name = 'persona/create.html'
    success_url = reverse_lazy('asys:miembro_list')
    url_redirect = success_url

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar miembro'
        context['entity'] = 'Miembros'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context

class MembersDelete(DeleteView):
    model = Miembro
    template_name = 'persona/delete.html'
    success_url = reverse_lazy('asys:miembro_list')
    url_redirect = success_url

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'delete':
                self.object.delete()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Borrando miembro'
        context['entity'] = 'Miembros'
        context['list_url'] = self.success_url
        context['action'] = 'delete'
        return context






