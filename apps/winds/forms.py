# winds/forms.py

from django import forms
from .models import Wind
from apps.tareas.models import Tarea
from apps.notas.models import Nota



class WindForm(forms.ModelForm):
    class Meta:
        model = Wind
        fields = ['titulo', 'descripcion', 'tareas', 'notas', 'pomodoro', 'focus_mode']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'tareas': forms.CheckboxSelectMultiple(),
            'notas': forms.CheckboxSelectMultiple(),
            'pomodoro': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        perfil = kwargs.pop('perfil', None)
        super().__init__(*args, **kwargs)

        if perfil:
            self.fields['tareas'].queryset = Tarea.objects.filter(perfil=perfil)
            self.fields['notas'].queryset = Nota.objects.filter(perfil=perfil)
            self.fields['pomodoro'].required = True
            self.fields['pomodoro'].empty_label = "Selecciona un Pomodoro"


class WindGrupoForm(forms.ModelForm):
    usuarios = forms.ModelMultipleChoiceField(queryset=None, widget=forms.SelectMultiple(attrs={'class': 'form-select'}))

    def __init__(self, *args, **kwargs):
        grupo = kwargs.pop('grupo')
        super().__init__(*args, **kwargs)
        self.fields['usuarios'].queryset = grupo.usuarios.all()
        self.fields['tareas'].queryset = Tarea.objects.filter(perfil__in=grupo.usuarios.all())
        self.fields['notas'].queryset = Nota.objects.filter(perfil__in=grupo.usuarios.all())

    class Meta:
        model = Wind
        fields = ['titulo', 'descripcion', 'tareas', 'notas', 'pomodoro', 'focus_mode']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 2}),
            'tareas': forms.CheckboxSelectMultiple(),
            'notas': forms.CheckboxSelectMultiple(),
        }
