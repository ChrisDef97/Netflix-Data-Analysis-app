"""
Constantes de configuracion y paleta de colores de la aplicacion.
"""

# --- comportamiento del analisis ---
UMBRAL_MINUTOS = 5
PALABRAS_EXCLUIDAS = ['trailer', 'teaser', 'clip', 'recap', 'hook', 'bonus video', 'backfill', 'unknown title']
COLUMNAS_REQUERIDAS = ['Title', 'Duration', 'Start Time']

# --- textos de la interfaz ---
PLACEHOLDER = 'Seleccione la serie/pelicula a analizar'
URL_NETFLIX_DATOS = 'https://www.netflix.com/account/getmyinfo'

# --- paleta de colores (modo oscuro) ---
COLOR_FONDO = "#1e1e1e"
COLOR_FONDO_GRAFICA = "#2b2b2b"
COLOR_TEXTO = "#e0e0e0"
COLOR_LINK = "#4da6ff"
COLOR_BARRA = "#4A55A2"
COLOR_EJE_X = "#F0BD50"
COLOR_EJE_Y = "#F0BD50"
COLOR_GRID = "#555555"
COLOR_BOTON_BG = "#333333"
COLOR_BOTON_FG = "#e0e0e0"
COLOR_BOTON_ACTIVO = "#444444"
COLOR_ERROR = "#ff6b6b"