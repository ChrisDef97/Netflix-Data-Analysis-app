"""
Logica de procesamiento de datos y ajustes de graficas, independiente de tkinter.
"""

import pandas as pd
from config import UMBRAL_MINUTOS, PALABRAS_EXCLUIDAS, COLUMNAS_REQUERIDAS


def procesar_csv(ruta):
    """
    Lee y limpia el CSV de Netflix.

    Devuelve una tupla (dataframe procesado, nombres por clave, lista de claves filtradas).
    Lanza ValueError si faltan columnas esperadas o si ninguna serie/pelicula
    supera el umbral minimo de tiempo visto.
    """
    datos = pd.read_csv(ruta, encoding='utf-8')

    columnas_faltantes = [c for c in COLUMNAS_REQUERIDAS if c not in datos.columns]
    if columnas_faltantes:
        raise ValueError(
            f"El archivo no tiene las columnas esperadas ({', '.join(columnas_faltantes)}). "
            "Verifica que sea el CSV 'ViewingActivity' de Netflix."
        )

    datos['Show'] = datos['Title'].str.split(':').str[0].str.strip()
    datos['Show_key'] = datos['Show'].str.lower()
    datos['Duration'] = pd.to_timedelta(datos['Duration'])

    tiempo_por_key = datos.groupby('Show_key')['Duration'].sum()
    keys_vistas = tiempo_por_key[tiempo_por_key > pd.Timedelta(minutes=UMBRAL_MINUTOS)].index

    nombres = datos.groupby('Show_key')['Show'].agg(lambda x: x.value_counts().index[0])

    keys_filtradas = sorted(
        k for k in keys_vistas
        if not any(palabra in k for palabra in PALABRAS_EXCLUIDAS)
    )

    if not keys_filtradas:
        raise ValueError("No se encontraron series o peliculas con suficiente tiempo visto en este archivo.")

    return datos, nombres, keys_filtradas


def formatear_hora(hora):
    """Convierte una hora en formato 24h (0-23) a texto en formato 12h (ej. '3pm')."""
    if hora == 0:
        return '12am'
    elif hora < 12:
        return f'{hora}am'
    elif hora == 12:
        return '12pm'
    else:
        return f'{hora - 12}pm'


def formatear_duracion(duracion):
    """Convierte un Timedelta de pandas a texto legible tipo 'Xh Ymin'."""
    total_minutos = int(duracion.total_seconds() // 60)
    horas = total_minutos // 60
    minutos = total_minutos % 60
    return f'{horas}h {minutos}min'


def asegurar_espacio_superior(ax):
    """Extiende el eje Y si la barra mas alta alcanza o supera el ultimo numero visible."""
    _, vmax = ax.get_ylim()
    ticks = ax.get_yticks()
    ticks_visibles = [t for t in ticks if t <= vmax]

    paso = ticks[1] - ticks[0] if len(ticks) > 1 else 1
    max_dato = max((patch.get_height() for patch in ax.patches), default=0)
    ultimo_visible = ticks_visibles[-1] if ticks_visibles else vmax

    if max_dato >= ultimo_visible:
        ax.set_ylim(top=ultimo_visible + paso)


def centrar_ejes_horizontalmente(ax):
    """Centra el area de la grafica dentro del lienzo, sin invadir el espacio del label del eje Y."""
    pos = ax.get_position()
    nuevo_ancho = 1 - 2 * pos.x0
    ax.set_position([pos.x0, pos.y0, nuevo_ancho, pos.height])