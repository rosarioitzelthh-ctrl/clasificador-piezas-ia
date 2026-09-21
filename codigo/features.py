# features.py
# Calcula características de tiempo y de frecuencia para cada ventana

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


# ============================================================
# RUTAS
# ============================================================

carpeta_codigo = os.path.dirname(os.path.abspath(__file__))
carpeta_proyecto = os.path.dirname(carpeta_codigo)

carpeta_datos = os.path.join(carpeta_proyecto, 'datos')
carpeta_figuras = os.path.join(carpeta_proyecto, 'figuras')

ruta_entrada = os.path.join(carpeta_datos, 'datos_limpios.csv')
ruta_salida = os.path.join(carpeta_datos, 'features.csv')

os.makedirs(carpeta_figuras, exist_ok=True)


# ============================================================
# CONFIGURACION
# ============================================================

FS = 100.0       # Frecuencia de muestreo aproximada
UMBRAL = 5


# ============================================================
# COMPROBAR ARCHIVO
# ============================================================

if not os.path.exists(ruta_entrada):
    print("No se encontro datos_limpios.csv")
    print("Primero ejecuta limpiar.py")
    exit()


# ============================================================
# LEER DATOS
# ============================================================

datos = pd.read_csv(ruta_entrada)

print("======================================")
print("   CALCULANDO FEATURES")
print("======================================")


# ============================================================
# CALCULAR FEATURES
# ============================================================

filas = []

for ventana, g in datos.groupby('ventana'):

    x = g['valor'].values
    etiqueta = g['etiqueta'].iloc[0]

    # --------------------------------------------------------
    # FEATURES DE TIEMPO
    # --------------------------------------------------------

    media = x.mean()
    desv = x.std()
    minimo = x.min()
    maximo = x.max()
    rango = maximo - minimo
    energia = np.sum(x ** 2)
    duracion = np.sum(np.abs(x) > UMBRAL)

    # --------------------------------------------------------
    # FFT
    # --------------------------------------------------------

    espectro = np.abs(np.fft.rfft(x))[1:]

    frecuencias = np.fft.rfftfreq(
        len(x),
        1 / FS
    )[1:]

    # Frecuencia dominante
    if len(espectro) > 0:
        f_dominante = frecuencias[np.argmax(espectro)]
    else:
        f_dominante = 0

    # Centroide espectral
    if np.sum(espectro) > 0:
        centroide = np.sum(
            frecuencias * espectro
        ) / np.sum(espectro)
    else:
        centroide = 0

    # Energia espectral
    energia_espectral = np.sum(espectro ** 2)

    # --------------------------------------------------------
    # BANDAS DE FRECUENCIA
    # --------------------------------------------------------

    banda_baja = np.sum(
        espectro[
            (frecuencias >= 0) &
            (frecuencias < 10)
        ] ** 2
    )

    banda_media = np.sum(
        espectro[
            (frecuencias >= 10) &
            (frecuencias < 25)
        ] ** 2
    )

    banda_alta = np.sum(
        espectro[
            (frecuencias >= 25) &
            (frecuencias <= 50)
        ] ** 2
    )

    # --------------------------------------------------------
    # GUARDAR FILA
    # --------------------------------------------------------

    fila = {
        'ventana': ventana,

        # Tiempo
        'media': media,
        'desv': desv,
        'minimo': minimo,
        'maximo': maximo,
        'rango': rango,
        'energia': energia,
        'duracion': duracion,

        # Frecuencia
        'f_dominante': f_dominante,
        'centroide': centroide,
        'energia_espectral': energia_espectral,
        'banda_baja': banda_baja,
        'banda_media': banda_media,
        'banda_alta': banda_alta,

        'etiqueta': etiqueta
    }

    filas.append(fila)


# ============================================================
# CREAR TABLA
# ============================================================

features = pd.DataFrame(filas)


# ============================================================
# GUARDAR FEATURES
# ============================================================

try:

    features.to_csv(
        ruta_salida,
        index=False
    )

    print("\nFeatures guardadas correctamente:")
    print(ruta_salida)

except PermissionError:

    print("\nERROR: No se pudo guardar features.csv")
    print("Cierra features.csv si esta abierto en Excel o VS Code.")
    exit()


# ============================================================
# INFORMACION
# ============================================================

print("\n======================================")
print("      FEATURES CALCULADAS")
print("======================================")

print("\nPrimeras filas:")
print(features.head())

print("\nTamaño de la tabla:")
print(f"Filas: {features.shape[0]}")
print(f"Columnas: {features.shape[1]}")

print("\nVentanas por clase:")
print(features.groupby('etiqueta').size())


print("\nColumnas:")
for columna in features.columns:
    print("-", columna)


# ============================================================
# GRAFICAS DE FEATURES DE TIEMPO
# ============================================================

pares = [
    ('rango', 'duracion'),
    ('minimo', 'rango'),
    ('desv', 'energia')
]

nombres = [
    'Rango vs Duracion',
    'Minimo vs Rango',
    'Desviacion vs Energia'
]


for i in range(len(pares)):

    eje_x = pares[i][0]
    eje_y = pares[i][1]

    plt.figure(figsize=(10, 7))

    for etiqueta, g in features.groupby('etiqueta'):

        plt.scatter(
            g[eje_x],
            g[eje_y],
            label=etiqueta
        )

    plt.xlabel(eje_x)
    plt.ylabel(eje_y)
    plt.title(nombres[i])
    plt.legend()
    plt.grid()

    nombre_archivo = (
        f"features_{eje_x}_vs_{eje_y}.png"
    )

    ruta_figura = os.path.join(
        carpeta_figuras,
        nombre_archivo
    )

    plt.savefig(
        ruta_figura,
        dpi=300,
        bbox_inches='tight'
    )

    plt.close()

    print("\nGrafica guardada:")
    print(ruta_figura)


# ============================================================
# GRAFICA DEL ESPECTRO
# ============================================================

print("\n======================================")
print("       GENERANDO ESPECTRO")
print("======================================")


plt.figure(figsize=(12, 7))

clases_encontradas = datos['etiqueta'].dropna().unique()


for etiqueta in clases_encontradas:

    # Tomar la primera ventana de esa clase
    ventanas_clase = datos[
        datos['etiqueta'] == etiqueta
    ]['ventana'].unique()

    if len(ventanas_clase) == 0:
        continue

    ventana = ventanas_clase[0]

    grupo = datos[
        (datos['ventana'] == ventana) &
        (datos['etiqueta'] == etiqueta)
    ]

    x = grupo['valor'].values

    if len(x) < 2:
        continue

    # FFT
    espectro = np.abs(
        np.fft.rfft(x)
    )[1:]

    frecuencias = np.fft.rfftfreq(
        len(x),
        1 / FS
    )[1:]

    # Graficar
    plt.plot(
        frecuencias,
        espectro,
        label=etiqueta
    )


plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Magnitud')
plt.title('Espectro de frecuencia por clase')

plt.xlim(0, 50)

plt.legend()
plt.grid()

ruta_espectro = os.path.join(
    carpeta_figuras,
    'espectro.png'
)

plt.savefig(
    ruta_espectro,
    dpi=300,
    bbox_inches='tight'
)

plt.close()


print("\n======================================")
print("      ESPECTRO GENERADO")
print("======================================")

print(ruta_espectro)


# ============================================================
# TERMINADO
# ============================================================

print("\n======================================")
print("       PROCESO TERMINADO")
print("======================================")

print("\nArchivos generados en:")
print(carpeta_figuras)

print("\nBusca estas graficas:")

print("- features_rango_vs_duracion.png")
print("- features_minimo_vs_rango.png")
print("- features_desv_vs_energia.png")
print("- espectro.png")

print("\nListo.")