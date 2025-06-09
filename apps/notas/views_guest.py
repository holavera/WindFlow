from django.views import View
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from .models import NotaSession



class GuestNotasView(View):
    def get(self, request):
        notas = NotaSession.obtener_todas(request)
        return render(request, 'notas/guest_dashboard_notas.html', {'notas': notas})

    def post(self, request):
        contenido = request.POST.get("contenido", "").strip()
        if contenido:
            nota = NotaSession.crear(request.POST)
            NotaSession.guardar(request, nota)
        return redirect('guest_notas')


@method_decorator(require_POST, name='dispatch')
class EliminarNotaGuestView(View):
    def post(self, request):
        nota_id = request.POST.get("nota_id")
        if nota_id:
            NotaSession.eliminar(request, nota_id)
        return redirect('guest_notas')


@method_decorator(require_POST, name='dispatch')
class EditarNotaGuestView(View):
    def post(self, request, nota_id):
        nuevo_contenido = request.POST.get("contenido", "").strip()
        if nuevo_contenido:
            NotaSession.editar(request, nota_id, nuevo_contenido)
        return redirect('guest_notas')
