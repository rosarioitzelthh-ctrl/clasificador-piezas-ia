# features.py
# Convierte cada ventana de datos en una fila de características

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


# ======================================
# RUTAS
# ======================================

carpeta_codigo = os.path.dirname(os.path.abspath(__file__))
carpeta_proyecto = os.path.dirname(carpeta_codigo)

carpeta_datos = os.path.join(carpeta_proyecto, 'datos')
carpeta_figuras = os.path.join(carpeta_proyecto, 'figuras')

ruta_entrada = os.path.join(carpeta_datos, 'datos_limpios.csv')
ruta_salida = os.path.join(carpeta_datos, 'features.csv')

os.makedirs(carpeta_figuras, exist_ok=True)


# ======================================
# COMPROBAR QUE EXISTE EL ARCHIVO
# ======================================

if not os.path.exists(ruta_entrada):
    print("No se encontro datos_limpios.csv.")
    print("Primero ejecuta limpiar.py.")
    exit()


# ======================================
# LEER LOS DATOS
# ======================================

datos = pd.read_csv(ruta_entrada)


# ======================================
# CALCULAR CARACTERISTICAS
# ======================================

filas = []

# Umbral utilizado para calcular la duracion
UMBRAL = 5

for ventana, g in datos.groupby('ventana'):

    x = g['valor'].values

    etiqueta = g['etiqueta'].iloc[0]

    fila = {
        'ventana': ventana,
        'media': x.mean(),
        'desv': x.std(),
        'minimo': x.min(),
        'maximo': x.max(),
        'rango': x.max() - x.min(),
        'energia': np.sum(x ** 2),
        'duracion': np.sum(np.abs(x) > UMBRAL),
        'etiqueta': etiqueta
    }

    filas.append(fila)


# ======================================
# CREAR TABLA DE CARACTERISTICAS
# ======================================

features = pd.DataFrame(filas)


# ======================================
# GUARDAR FEATURES.CSV
# ======================================

features.to_csv(ruta_salida, index=False)


# ======================================
# MOSTRAR RESULTADOS
# ======================================

print("======================================")
print("      FEATURES CALCULADAS")
print("======================================")

print("\nPrimeras filas:")
print(features.head())

print("\nTamaño de la tabla:")
print(f"Filas: {features.shape[0]}")
print(f"Columnas: {features.shape[1]}")

print("\nVentanas por clase:")
print(features.groupby('etiqueta').size())


# ======================================
# PROBAR 3 PARES DE CARACTERISTICAS
# ======================================

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


# ======================================
# CREAR LAS 3 GRAFICAS
# ======================================

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

    nombre_archivo = f"features_{eje_x}_vs_{eje_y}.png"

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

    print(f"\nGrafica guardada:")
    print(ruta_figura)


# ======================================
# TERMINADO
# ======================================

print("\n======================================")
print("       PROCESO TERMINADO")
print("======================================")

print("\nArchivo generado:")
print(ruta_salida)

print("\nSe probaron 3 pares de caracteristicas:")

for par in pares:
    print(f"- {par[0]} vs {par[1]}")

print("\nRevisa las 3 graficas dentro de la carpeta:")
print(carpeta_figuras)