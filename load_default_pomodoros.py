from apps.pomodoro.models import ConfiguracionPomodoro

def run():
    if not ConfiguracionPomodoro.objects.exists():
        ConfiguracionPomodoro.objects.create(
            nombre='Clásico 25/5/15',
            foco_min=25,
            descanso_corto_min=5,
            descanso_largo_min=15,
            ciclos=3
        )
        ConfiguracionPomodoro.objects.create(
            nombre='Intenso 40/10/15',
            foco_min=40,
            descanso_corto_min=10,
            descanso_largo_min=15,
            ciclos=2
        )
        ConfiguracionPomodoro.objects.create(
            nombre='Mini_Tiempo 1/0.5/1',
            foco_min=1,
            descanso_corto_min=0.5,
            descanso_largo_min=1,
            ciclos=3
        )
        print("Pomodoros por defecto cargados.")
    else:
        print("Pomodoros ya existentes. Nada que cargar.")
