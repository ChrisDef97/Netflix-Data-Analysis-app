"""
Analizador de Netflix — interfaz grafica.

Permite cargar el archivo ViewingActivity.csv exportado desde Netflix,
elegir una serie o pelicula, y visualizar cuando se vio: por dia de la
semana y por hora del dia.
"""

import tkinter as tk
from tkinter import filedialog, ttk
import webbrowser

import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MaxNLocator
from tkinterdnd2 import DND_FILES, TkinterDnD

from config import (
    UMBRAL_MINUTOS, PALABRAS_EXCLUIDAS, PLACEHOLDER, URL_NETFLIX_DATOS, COLUMNAS_REQUERIDAS,
    COLOR_FONDO, COLOR_FONDO_GRAFICA, COLOR_TEXTO, COLOR_LINK, COLOR_BARRA,
    COLOR_EJE_X, COLOR_EJE_Y, COLOR_GRID, COLOR_BOTON_BG, COLOR_BOTON_FG,
    COLOR_BOTON_ACTIVO, COLOR_ERROR
)
from analisis import (
    procesar_csv, formatear_hora, formatear_duracion,
    asegurar_espacio_superior, centrar_ejes_horizontalmente
)

# --- estado global de la aplicacion ---
df = None
nombre_mostrado = None
fig_dia = None
fig_hora = None


# =========================================================
# Carga de archivos
# =========================================================

def cargar_archivo(ruta):
    """Procesa el CSV elegido (por boton o drag-and-drop) y actualiza la interfaz."""
    global df, nombre_mostrado

    if not ruta.lower().endswith('.csv'):
        label_estado.config(text="El archivo debe ser un CSV.")
        return

    try:
        datos, nombres, keys_filtradas = procesar_csv(ruta)
    except FileNotFoundError:
        label_estado.config(text="No se pudo encontrar el archivo seleccionado.")
        return
    except UnicodeDecodeError:
        label_estado.config(text="No se pudo leer el archivo. Verifica que sea el CSV original de Netflix.")
        return
    except pd.errors.EmptyDataError:
        label_estado.config(text="El archivo esta vacio.")
        return
    except pd.errors.ParserError:
        label_estado.config(text="El archivo no tiene un formato de CSV valido.")
        return
    except ValueError as error:
        label_estado.config(text=str(error))
        return
    except Exception:
        label_estado.config(text="Ocurrio un error inesperado al procesar el archivo.")
        return

    df = datos
    nombre_mostrado = nombres

    label_ruta.config(text=ruta)
    label_estado.config(text="")

    nombres_para_mostrar = [nombre_mostrado[k] for k in keys_filtradas]
    combo['values'] = nombres_para_mostrar
    combo.set(PLACEHOLDER)
    combo.config(state='readonly')


def seleccionar_archivo():
    """Callback del boton 'Seleccionar CSV': abre el explorador de archivos nativo."""
    ruta = filedialog.askopenfilename(
        title="Selecciona tu archivo CSV de Netflix",
        filetypes=[("Archivos CSV", "*.csv")]
    )
    if ruta:
        cargar_archivo(ruta)


def manejar_drop(event):
    """Callback de drag-and-drop: se dispara al soltar un archivo sobre la ventana."""
    rutas = ventana.tk.splitlist(event.data)
    if rutas:
        cargar_archivo(rutas[0])


def abrir_link_netflix(event=None):
    """Abre en el navegador la pagina de Netflix para solicitar los datos personales."""
    webbrowser.open(URL_NETFLIX_DATOS)


# =========================================================
# Analisis y generacion de graficas
# =========================================================

def analizar():
    """Callback del boton 'Analizar': filtra la serie elegida y genera ambas graficas."""
    global fig_dia, fig_hora

    nombre_elegido = combo.get()
    if nombre_elegido == PLACEHOLDER or not nombre_elegido:
        label_estado.config(text="Primero elige una serie/pelicula de la lista.")
        return

    key_elegida = nombre_elegido.lower()
    serie = df[df['Show_key'] == key_elegida]
    serie = serie[serie['Duration'] > '0 days 00:01:00']

    tiempo_total = serie['Duration'].sum()
    total_episodios = len(serie)

    serie = serie.copy()
    serie['weekday'] = serie['Start Time'].apply(lambda x: pd.to_datetime(x, utc=True))
    serie['weekday'] = serie['weekday'].dt.tz_convert('Europe/Madrid')
    serie['hour'] = serie['weekday'].dt.hour
    serie['weekday'] = serie['weekday'].dt.weekday

    # --- grafico por dia de la semana ---
    dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    serie['weekday'] = pd.Categorical(serie['weekday'], categories=[0, 1, 2, 3, 4, 5, 6], ordered=True)
    serie_by_day = serie['weekday'].value_counts().sort_index()
    serie_by_day.index = dias_semana

    fig_dia = Figure(figsize=(12, 4.3))
    fig_dia.patch.set_facecolor(COLOR_FONDO_GRAFICA)
    ax1 = fig_dia.add_subplot(111)
    ax1.set_facecolor(COLOR_FONDO_GRAFICA)
    ax1.bar(serie_by_day.index, serie_by_day.values, color=COLOR_BARRA)

    fig_dia.suptitle(f'Episodios vistos de {nombre_elegido} por dia de la semana',
                      fontsize=14, color=COLOR_TEXTO, y=0.93)
    ax1.set_title(f'Total de episodios: {total_episodios}', fontsize=11, color=COLOR_TEXTO, pad=12)
    ax1.set_xlabel('Dia de la semana', labelpad=15, color=COLOR_EJE_X)
    ax1.set_ylabel('Episodios', rotation=0, labelpad=40, color=COLOR_EJE_Y)
    ax1.tick_params(axis='x', colors=COLOR_EJE_X)
    ax1.tick_params(axis='y', colors=COLOR_EJE_Y)
    ax1.yaxis.set_major_locator(MaxNLocator(integer=True))
    asegurar_espacio_superior(ax1)
    ax1.set_axisbelow(True)
    ax1.grid(axis='y', linestyle='--', alpha=0.4, color=COLOR_GRID)
    for spine in ax1.spines.values():
        spine.set_color(COLOR_GRID)
    fig_dia.tight_layout(rect=[0, 0, 1, 0.93])
    centrar_ejes_horizontalmente(ax1)

    # --- grafico por hora del dia ---
    horas_formateadas = [formatear_hora(h) for h in range(24)]
    serie['hour'] = pd.Categorical(serie['hour'], categories=list(range(24)), ordered=True)
    serie_by_hour = serie['hour'].value_counts().sort_index()
    serie_by_hour.index = horas_formateadas

    fig_hora = Figure(figsize=(12, 4.3))
    fig_hora.patch.set_facecolor(COLOR_FONDO_GRAFICA)
    ax2 = fig_hora.add_subplot(111)
    ax2.set_facecolor(COLOR_FONDO_GRAFICA)
    ax2.bar(serie_by_hour.index, serie_by_hour.values, color=COLOR_BARRA)

    fig_hora.suptitle(f'Episodios vistos de {nombre_elegido} por hora',
                       fontsize=14, color=COLOR_TEXTO, y=0.93)
    ax2.set_title(f'Total de horas vistas: {formatear_duracion(tiempo_total)}',
                  fontsize=11, color=COLOR_TEXTO, pad=12)
    ax2.set_xlabel('Hora del dia', labelpad=15, color=COLOR_EJE_X)
    ax2.set_ylabel('Episodios', rotation=0, labelpad=40, color=COLOR_EJE_Y)
    ax2.tick_params(axis='x', labelsize=9, colors=COLOR_EJE_X)
    ax2.tick_params(axis='y', colors=COLOR_EJE_Y)
    ax2.margins(x=0.01)
    ax2.yaxis.set_major_locator(MaxNLocator(integer=True))
    asegurar_espacio_superior(ax2)
    ax2.set_axisbelow(True)
    ax2.grid(axis='y', linestyle='--', alpha=0.4, color=COLOR_GRID)
    for spine in ax2.spines.values():
        spine.set_color(COLOR_GRID)
    fig_hora.tight_layout(rect=[0, 0, 1, 0.93])
    centrar_ejes_horizontalmente(ax2)

    # --- mostrar ambas graficas en la ventana ---
    for widget in frame_graficos.winfo_children():
        widget.destroy()

    canvas1 = FigureCanvasTkAgg(fig_dia, master=frame_graficos)
    canvas1.draw()
    canvas1.get_tk_widget().pack(pady=5)
    tk.Button(frame_graficos, text="Guardar grafico por dia", command=guardar_grafico_dia,
              bg=COLOR_BOTON_BG, fg=COLOR_BOTON_FG, activebackground=COLOR_BOTON_ACTIVO,
              activeforeground=COLOR_BOTON_FG, relief='flat', bd=0, padx=8, pady=4,
              cursor="hand2").pack(pady=(5, 15))

    canvas2 = FigureCanvasTkAgg(fig_hora, master=frame_graficos)
    canvas2.draw()
    canvas2.get_tk_widget().pack(pady=(15, 5))
    tk.Button(frame_graficos, text="Guardar grafico por hora", command=guardar_grafico_hora,
              bg=COLOR_BOTON_BG, fg=COLOR_BOTON_FG, activebackground=COLOR_BOTON_ACTIVO,
              activeforeground=COLOR_BOTON_FG, relief='flat', bd=0, padx=8, pady=4,
              cursor="hand2").pack(pady=5)

    label_estado.config(text="")


def guardar_grafico_dia():
    """Callback para exportar la grafica por dia como PNG, manteniendo el fondo oscuro."""
    ruta = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("Imagen PNG", "*.png")],
        initialfile="episodios_por_dia.png"
    )
    if ruta:
        fig_dia.savefig(ruta, facecolor=fig_dia.get_facecolor())


def guardar_grafico_hora():
    """Callback para exportar la grafica por hora como PNG, manteniendo el fondo oscuro."""
    ruta = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("Imagen PNG", "*.png")],
        initialfile="episodios_por_hora.png"
    )
    if ruta:
        fig_hora.savefig(ruta, facecolor=fig_hora.get_facecolor())


# =========================================================
# Construccion de la ventana
# =========================================================

ventana = TkinterDnD.Tk()
ventana.title("Analizador de Netflix")
ventana.geometry("1200x750")
ventana.configure(bg=COLOR_FONDO)
ventana.drop_target_register(DND_FILES)
ventana.dnd_bind('<<Drop>>', manejar_drop)

# --- estilo ttk (Combobox y Scrollbar no aceptan bg/fg directo) ---
style = ttk.Style()
style.theme_use('clam')

style.configure('TCombobox',
                 fieldbackground=COLOR_FONDO_GRAFICA,
                 background=COLOR_FONDO_GRAFICA,
                 foreground=COLOR_TEXTO,
                 arrowcolor=COLOR_TEXTO,
                 bordercolor=COLOR_FONDO_GRAFICA,
                 lightcolor=COLOR_FONDO_GRAFICA,
                 darkcolor=COLOR_FONDO_GRAFICA)
style.map('TCombobox',
          fieldbackground=[('readonly', COLOR_FONDO_GRAFICA)],
          foreground=[('readonly', COLOR_TEXTO)])

style.configure('TScrollbar',
                 background=COLOR_BOTON_BG,
                 troughcolor=COLOR_FONDO,
                 bordercolor=COLOR_FONDO,
                 arrowcolor=COLOR_TEXTO)

# la lista desplegable del combobox es un Listbox clasico, se pinta aparte
ventana.option_add('*TCombobox*Listbox.background', COLOR_FONDO_GRAFICA)
ventana.option_add('*TCombobox*Listbox.foreground', COLOR_TEXTO)
ventana.option_add('*TCombobox*Listbox.selectBackground', COLOR_BOTON_ACTIVO)
ventana.option_add('*TCombobox*Listbox.selectForeground', COLOR_TEXTO)

# --- seccion informativa: como descargar los datos de Netflix ---
frame_info = tk.Frame(ventana, bg=COLOR_FONDO)
frame_info.pack(pady=(10, 0), padx=(180, 20), fill='x')

texto_info = ("Si no posees tus datos personales de Netflix, puedes solicitarlos accediendo al siguiente enlace, "
              "siempre que hayas iniciado sesion previamente.\n"
              "El proceso de generacion suele completarse en menos de 24 horas, aunque Netflix indica que puede "
              "demorar hasta 30 dias.")
label_info = tk.Label(frame_info, text=texto_info, justify='left', wraplength=900,
                       font=('TkDefaultFont', 11), bg=COLOR_FONDO, fg=COLOR_TEXTO)
label_info.pack(anchor='w')

link_info = tk.Label(frame_info, text=URL_NETFLIX_DATOS, fg=COLOR_LINK, bg=COLOR_FONDO, cursor="hand2",
                      font=('TkDefaultFont', 11, 'underline'))
link_info.pack(anchor='w')
link_info.bind("<Button-1>", abrir_link_netflix)

label_archivo_info = tk.Label(
    frame_info,
    text=("El archivo que necesitas se llama 'ViewingActivity.csv' y se encuentra dentro de la carpeta "
          "'CONTENT_INTERACTION' una vez descargados tus datos."),
    justify='left', wraplength=900, font=('TkDefaultFont', 10), bg=COLOR_FONDO, fg=COLOR_TEXTO
)
label_archivo_info.pack(anchor='w', pady=(5, 0))

# --- controles principales ---
boton = tk.Button(ventana, text="Seleccionar CSV", command=seleccionar_archivo,
                   bg=COLOR_BOTON_BG, fg=COLOR_BOTON_FG, activebackground=COLOR_BOTON_ACTIVO,
                   activeforeground=COLOR_BOTON_FG, relief='flat', bd=0, padx=10, pady=5,
                   cursor="hand2")
boton.pack(pady=10)

label_hint = tk.Label(ventana, text="(tambien puedes arrastrar tu archivo CSV a cualquier parte de la ventana)",
                       font=('TkDefaultFont', 9), bg=COLOR_FONDO, fg=COLOR_TEXTO)
label_hint.pack(pady=(0, 5))

label_ruta = tk.Label(ventana, text="Ningun archivo seleccionado", wraplength=1150,
                       bg=COLOR_FONDO, fg=COLOR_TEXTO)
label_ruta.pack(pady=5)

combo = ttk.Combobox(ventana, state='disabled', width=50, justify='center')
combo.set(PLACEHOLDER)
combo.pack(pady=5)

boton_analizar = tk.Button(ventana, text="Analizar", command=analizar,
                            bg=COLOR_BOTON_BG, fg=COLOR_BOTON_FG, activebackground=COLOR_BOTON_ACTIVO,
                            activeforeground=COLOR_BOTON_FG, relief='flat', bd=0, padx=10, pady=5,
                            cursor="hand2")
boton_analizar.pack(pady=5)

label_estado = tk.Label(ventana, text="", fg=COLOR_ERROR, bg=COLOR_FONDO)
label_estado.pack()

# --- area scrolleable para las graficas ---
contenedor_scroll = tk.Frame(ventana, bg=COLOR_FONDO)
contenedor_scroll.pack(fill='both', expand=True, pady=5)

scroll_canvas = tk.Canvas(contenedor_scroll, bg=COLOR_FONDO, highlightthickness=0)
scrollbar = ttk.Scrollbar(contenedor_scroll, orient='vertical', command=scroll_canvas.yview)
scroll_canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side='right', fill='y')
scroll_canvas.pack(side='left', fill='both', expand=True)

frame_graficos = tk.Frame(scroll_canvas, bg=COLOR_FONDO)
ventana_frame_id = scroll_canvas.create_window((0, 0), window=frame_graficos, anchor='nw')


def actualizar_scrollregion(event):
    scroll_canvas.configure(scrollregion=scroll_canvas.bbox('all'))


def ajustar_ancho_frame(event):
    scroll_canvas.itemconfig(ventana_frame_id, width=event.width)


frame_graficos.bind('<Configure>', actualizar_scrollregion)
scroll_canvas.bind('<Configure>', ajustar_ancho_frame)


def on_mousewheel(event):
    scroll_canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units')


scroll_canvas.bind_all('<MouseWheel>', on_mousewheel)

ventana.mainloop()