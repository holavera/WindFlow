# tareas/forms.py
from django import forms
from .models import Tarea

class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['titulo', 'descripcion', 'fecha_limite']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'fecha_limite': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['titulo'].required = True
        self.fields['fecha_limite'].required = True

