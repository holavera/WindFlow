# usuarios/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class CustomUserCreationForm(UserCreationForm):
    ROL_CHOICES = [
        ('free', 'Usuario Gratuito'),
        ('admin_free', 'Administrador Gratuito'),
    ]

    rol_inicial = forms.ChoiceField(
        choices=ROL_CHOICES,
        label="Tipo de cuenta",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "rol_inicial")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True  # Hace el email obligatorio

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Ya existe un usuario con este correo electrónico.")
        return email