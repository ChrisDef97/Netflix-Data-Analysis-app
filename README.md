# 🎬 Analizador de Netflix / Netflix Viewing Analyzer

Aplicacion de escritorio para analizar tu historial personal de visualizacion de Netflix.
Desktop application to analyze your personal Netflix viewing history.

🇪🇸 [Español](#español) | 🇬🇧 [English](#english)

---

## Español

### ¿Qué hace este programa?

Analiza el archivo `ViewingActivity.csv` que Netflix genera cuando solicitas tus datos personales, y muestra:

- **Episodios vistos por día de la semana**
- **Episodios vistos por hora del día**
- Totales de episodios y tiempo visto para la serie o película que elijas

Todo con una interfaz grafica en modo oscuro, seleccion de archivo por boton o arrastrando el CSV directamente a la ventana, y la posibilidad de guardar cada grafica como imagen PNG.

### Como obtener tus datos de Netflix

1. Con tu sesion iniciada, entra a [netflix.com/account/getmyinfo](https://www.netflix.com/account/getmyinfo) y solicita tus datos.
2. El proceso suele tardar menos de 24 horas, aunque Netflix indica que puede demorar hasta 30 dias.
3. Dentro de la descarga, el archivo que necesitas es **`ViewingActivity.csv`**, ubicado en la carpeta **`CONTENT_INTERACTION`**.

### Como usarlo

**Opcion 1 — Descargar el ejecutable (recomendado, no requiere tener Python instalado)**

1. Ve a la seccion [Releases](../../releases) de este repositorio.
2. Descarga `AnalizadorDeNetflix.exe`.
3. Ejecutalo. Windows puede mostrar una advertencia de SmartScreen por ser un ejecutable sin firma digital — es normal, elige "Mas informacion" → "Ejecutar de todas formas".

**Opcion 2 — Ejecutar desde el codigo fuente**

```bash
git clone https://github.com/ChrisDef97/Netflix-Data-Analysis-app.git
cd Netflix-Data-Analysis-app
pip install -r requirements.txt
python gui.py
```

### Tecnologias utilizadas

- **Python** — logica y procesamiento de datos
- **pandas** — limpieza y analisis del CSV
- **matplotlib** — generacion de graficas
- **tkinter** + **tkinterdnd2** — interfaz grafica y soporte de drag-and-drop
- **PyInstaller** — empaquetado como ejecutable independiente

### Ideas para futuras versiones

- [ ] Soporte multi-idioma dentro de la propia aplicacion (selector de idioma en la interfaz)
- [ ] Analisis adicionales (por mes, por año, series mas vistas en total)

### Creditos

Proyecto iniciado como ejercicio de aprendizaje a partir del [tutorial de Dataquest sobre analisis de datos personales de Netflix](https://www.dataquest.io/blog/python-tutorial-analyze-personal-netflix-data/), y evolucionado significativamente mas alla del alcance original.

---

## English

### What does this program do?

Analyzes the `ViewingActivity.csv` file that Netflix generates when you request your personal data, and shows:

- **Episodes watched by day of the week**
- **Episodes watched by hour of the day**
- Totals of episodes and time watched for the show or movie you choose

All through a dark-mode graphical interface, with file selection via button or by dragging the CSV directly into the window, and the ability to save each chart as a PNG image.

### How to get your Netflix data

1. While logged in, go to [netflix.com/account/getmyinfo](https://www.netflix.com/account/getmyinfo) and request your data.
2. The process usually takes less than 24 hours, though Netflix states it can take up to 30 days.
3. Inside the download, the file you need is **`ViewingActivity.csv`**, located in the **`CONTENT_INTERACTION`** folder.

### How to use it

**Option 1 — Download the executable (recommended, no Python installation required)**

1. Go to the [Releases](../../releases) section of this repository.
2. Download `AnalizadorDeNetflix.exe`.
3. Run it. Windows may show a SmartScreen warning since it's an unsigned executable — this is expected, click "More info" → "Run anyway".

**Option 2 — Run from source**

```bash
git clone https://github.com/ChrisDef97/Netflix-Data-Analysis-app.git
cd Netflix-Data-Analysis-app
pip install -r requirements.txt
python gui.py
```

### Tech stack

- **Python** — core logic and data processing
- **pandas** — CSV cleaning and analysis
- **matplotlib** — chart generation
- **tkinter** + **tkinterdnd2** — graphical interface and drag-and-drop support
- **PyInstaller** — packaging as a standalone executable

### Ideas for future versions

- [ ] In-app multi-language support (language selector in the interface)
- [ ] Additional breakdowns (by month, by year, most-watched shows overall)

### Credits

Project started as a learning exercise based on [Dataquest's tutorial on analyzing personal Netflix data](https://www.dataquest.io/blog/python-tutorial-analyze-personal-netflix-data/), and significantly expanded beyond its original scope.
