# Generated by Django 5.2.1 on 2025-05-13 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tarea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('completada', models.BooleanField(default=False)),
                ('categoria', models.CharField(choices=[('personal', 'Personal'), ('trabajo', 'Trabajo'), ('estudio', 'Estudio'), ('otros', 'Otros')], default='personal', max_length=20)),
                ('fecha_limite', models.DateField(blank=True, null=True)),
                ('prioridad', models.IntegerField(default=1)),
            ],
        ),
    ]
