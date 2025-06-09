# admin_wind/forms.py

from django import forms
from .models import GrupoPersonal
from apps.winds.models import Wind
from apps.tareas.models import Tarea
from apps.notas.models import Nota
from apps.perfil.models import Perfil

class GrupoForm(forms.ModelForm):
    class Meta:
        model = GrupoPersonal
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'usuarios': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }


class AgregarUsuarioGrupoForm(forms.Form):
    query = forms.CharField(label="Nombre o Email del Usuario", max_length=100,
                            widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean_query(self):
        data = self.cleaned_data['query']
        try:
            return Perfil.objects.get(user__username=data)  # busca por username
        except Perfil.DoesNotExist:
            try:
                return Perfil.objects.get(user__email=data)  # busca por email
            except Perfil.DoesNotExist:
                raise forms.ValidationError("No se encontró ningún usuario con ese nombre o email.")


class CrearWindGrupoForm(forms.ModelForm):
    usuarios = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.SelectMultiple(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Wind
        fields = ['titulo', 'descripcion', 'tareas', 'notas', 'pomodoro', 'focus_mode']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tareas': forms.SelectMultiple(attrs={'class': 'form-select', 'id': 'id_tareas'}),
            'notas': forms.SelectMultiple(attrs={'class': 'form-select', 'id': 'id_notas'}),
            'pomodoro': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        grupo = kwargs.pop('grupo', None)
        if grupo is None:
            raise ValueError("Debes pasar 'grupo' como argumento al formulario CrearWindGrupoForm.")
        super().__init__(*args, **kwargs)
        self.fields['usuarios'].queryset = grupo.usuarios.all()
        self.fields['tareas'].queryset = Tarea.objects.filter(perfil__in=grupo.usuarios.all())
        self.fields['notas'].queryset = Nota.objects.filter(perfil__in=grupo.usuarios.all())
        self.fields['pomodoro'].required = True
        self.fields['pomodoro'].empty_label = "Selecciona un Pomodoro"




