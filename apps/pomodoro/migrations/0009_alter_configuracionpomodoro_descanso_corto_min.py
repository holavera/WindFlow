# Generated by Django 5.2.1 on 2025-05-26 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pomodoro', '0008_alter_sesionpomodoro_duracion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuracionpomodoro',
            name='descanso_corto_min',
            field=models.FloatField(default=5.0),
        ),
    ]
