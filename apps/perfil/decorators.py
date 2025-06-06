from django.shortcuts import redirect
from functools import wraps
from apps.perfil.models import Perfil



def solo_usuarios(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if hasattr(request.user, 'perfil') and request.user.perfil.rol in [
            Perfil.Rol.FREE_USER, Perfil.Rol.SUBSCRIBED_USER
        ]:
            return view_func(request, *args, **kwargs)
        return redirect('dashboard')
    return _wrapped_view


def solo_admins(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if hasattr(request.user, 'perfil') and request.user.perfil.rol in [
            Perfil.Rol.ADMIN_FREE, Perfil.Rol.ADMIN_SUBSCRIBED
        ]:
            return view_func(request, *args, **kwargs)
        return redirect('dashboard')
    return _wrapped_view


def solo_suscritos(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if hasattr(request.user, 'perfil') and request.user.perfil.rol in [
            Perfil.Rol.SUBSCRIBED_USER, Perfil.Rol.ADMIN_SUBSCRIBED
        ]:
            return view_func(request, *args, **kwargs)
        return redirect('upgrade')
    return _wrapped_view


def permitir_roles(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if hasattr(request.user, 'perfil') and request.user.perfil.rol in roles:
                return view_func(request, *args, **kwargs)
            return redirect('dashboard')
        return _wrapped_view
    return decorator

solo_basicos = permitir_roles(Perfil.Rol.FREE_USER)
solo_suscritos_puros = permitir_roles(Perfil.Rol.SUBSCRIBED_USER)
solo_admins_gratis = permitir_roles(Perfil.Rol.ADMIN_FREE)
solo_admins_suscritos = permitir_roles(Perfil.Rol.ADMIN_SUBSCRIBED)
solo_invitados = permitir_roles(Perfil.Rol.GUEST)
