"""Funcionalidad propia: resumen de cumplimiento de un reto.

Usa las mismas reglas del semáforo del frontend (core/semaforo.ts):
una semana cerrada queda en verde con 100 %, en rojo con menos de 10 % y en amarillo en otro caso.
"""
from django.utils import timezone

META = 100
UMBRAL_ROJO = 10


def color_semana(tarea, hoy):
    if hoy < tarea.fecha_inicio:
        return 'PENDIENTE'
    if hoy <= tarea.fecha_fin:
        return 'ABIERTA'
    if tarea.porcentaje >= META:
        return 'VERDE'
    if tarea.porcentaje < UMBRAL_ROJO:
        return 'ROJO'
    return 'AMARILLO'


def resumen_reto(reto, hoy=None):
    hoy = hoy or timezone.localdate()
    tareas = list(reto.tareas.order_by('semana'))
    colores = [color_semana(t, hoy) for t in tareas]
    cerradas = [t for t, c in zip(tareas, colores) if c in ('VERDE', 'AMARILLO', 'ROJO')]

    conteo = {c: colores.count(c) for c in ('VERDE', 'AMARILLO', 'ROJO', 'ABIERTA', 'PENDIENTE')}

    # Racha: semanas verdes seguidas, contando hacia atrás desde la última cerrada.
    racha = 0
    for color in reversed([c for c in colores if c in ('VERDE', 'AMARILLO', 'ROJO')]):
        if color != 'VERDE':
            break
        racha += 1

    cumplimiento = round(sum(t.porcentaje for t in cerradas) / len(cerradas)) if cerradas else None
    actual = next((t for t, c in zip(tareas, colores) if c == 'ABIERTA'), None)

    if cumplimiento is None:
        nivel = 'SIN_DATOS'
    elif cumplimiento >= 80:
        nivel = 'BUENO'
    elif cumplimiento >= 50:
        nivel = 'REGULAR'
    else:
        nivel = 'BAJO'

    return {
        'reto': reto.id,
        'total_semanas': len(tareas),
        'semanas_cerradas': len(cerradas),
        'semanas_restantes': conteo['ABIERTA'] + conteo['PENDIENTE'],
        'conteo': conteo,
        'cumplimiento': cumplimiento,
        'nivel': nivel,
        'racha_verde': racha,
        'semana_actual': actual.semana if actual else None,
        'porcentaje_actual': actual.porcentaje if actual else None,
        'total_avances': reto.avances.count(),
    }
