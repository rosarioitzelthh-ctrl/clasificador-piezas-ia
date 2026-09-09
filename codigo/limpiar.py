# limpiar.py - quita ruido, corrige la linea base y normaliza el dataset

import pandas as pd
import matplotlib.pyplot as plt
import os


# ==================================================
# 1. UBICAR LOS ARCHIVOS
# ==================================================

carpeta_codigo = os.path.dirname(os.path.abspath(__file__))
carpeta_proyecto = os.path.dirname(carpeta_codigo)

carpeta_datos = os.path.join(carpeta_proyecto, 'datos')
carpeta_figuras = os.path.join(carpeta_proyecto, 'figuras')

ruta_entrada = os.path.join(carpeta_datos, 'datos.csv')
ruta_salida = os.path.join(carpeta_datos, 'datos_limpios.csv')
ruta_figura = os.path.join(carpeta_figuras, 'limpieza.png')

os.makedirs(carpeta_figuras, exist_ok=True)


# ==================================================
# 2. LEER LOS DATOS
# ==================================================

if not os.path.exists(ruta_entrada):
    print("No se encontro datos.csv.")
    print("Primero ejecuta adquirir.py para capturar los datos.")
    exit()

datos = pd.read_csv(ruta_entrada)

print("Datos originales:")
print(datos.head())


# ==================================================
# 3. QUITAR VALORES FUERA DEL RANGO FISICO
# ==================================================

# El HC-SR04 mide distancia en centimetros.
# Se eliminan valores menores o iguales a 0
# y valores mayores a 400 cm.

datos = datos[
    (datos['valor'] > 0) &
    (datos['valor'] <= 400)
].copy()


# ==================================================
# 4. APLICAR FILTRO DE MEDIA MOVIL
# ==================================================

# Se utiliza una media movil de 5 muestras.
# Se aplica ventana por ventana para no mezclar
# los datos de diferentes piezas.

datos['valor_filtrado'] = (
    datos.groupby('ventana')['valor']
    .transform(
        lambda x: x.rolling(
            window=5,
            center=True
        ).mean()
    )
)


# ==================================================
# 5. ELIMINAR LOS NaN
# ==================================================

# La media movil deja valores vacios en las orillas
# de cada ventana.

datos = datos.dropna(
    subset=['valor_filtrado']
).copy()


# ==================================================
# 6. CALCULAR LA LINEA BASE
# ==================================================

# La linea base es el promedio de las primeras
# 20 muestras de cada ventana.

base = (
    datos[datos['t'] < 20]
    .groupby('ventana')['valor_filtrado']
    .mean()
)


# ==================================================
# 7. CORREGIR LA LINEA BASE
# ==================================================

# A cada muestra se le resta la linea base
# correspondiente a su propia ventana.

datos['valor_corregido'] = (
    datos['valor_filtrado']
    - datos['ventana'].map(base)
)


# ==================================================
# 8. NORMALIZAR
# ==================================================

# Se utiliza normalizacion min-max.
# Los valores de cada ventana quedan entre 0 y 1.

datos['valor_normalizado'] = (
    datos.groupby('ventana')['valor_corregido']
    .transform(
        lambda x:
        (x - x.min()) / (x.max() - x.min())
        if x.max() != x.min()
        else 0
    )
)


# ==================================================
# 9. CREAR GRAFICA DE ANTES Y DESPUES
# ==================================================

# Buscamos una clase que tenga al menos dos ventanas.

clase_ejemplo = datos['etiqueta'].iloc[0]

ventanas_clase = (
    datos[datos['etiqueta'] == clase_ejemplo]
    ['ventana']
    .unique()
)

if len(ventanas_clase) >= 2:

    ventana_inicial = ventanas_clase[0]
    ventana_final = ventanas_clase[-1]

    datos_inicial = datos[
        datos['ventana'] == ventana_inicial
    ]

    datos_final = datos[
        datos['ventana'] == ventana_final
    ]

    plt.figure(figsize=(10, 6))

    # Ventana inicial antes de limpiar
    plt.plot(
        datos_inicial['t'],
        datos_inicial['valor'],
        label=f'Inicial - ventana {ventana_inicial}'
    )

    # Ventana final antes de limpiar
    plt.plot(
        datos_final['t'],
        datos_final['valor'],
        label=f'Final - ventana {ventana_final}'
    )

    # Ventana inicial después de limpiar
    plt.plot(
        datos_inicial['t'],
        datos_inicial['valor_normalizado'],
        label='Inicial - normalizada'
    )

    # Ventana final después de limpiar
    plt.plot(
        datos_final['t'],
        datos_final['valor_normalizado'],
        label='Final - normalizada'
    )

    plt.xlabel('Muestra')
    plt.ylabel('Valor')
    plt.title(
        f'Comparacion antes y despues de limpiar - {clase_ejemplo}'
    )

    plt.legend()
    plt.grid()

    plt.savefig(
        ruta_figura,
        dpi=300,
        bbox_inches='tight'
    )

    plt.close()

    print("\nGrafica creada:")
    print(ruta_figura)

else:

    print("\nTodavia no hay dos ventanas de la misma clase.")
    print("La grafica se generara cuando tengas suficientes datos.")


# ==================================================
# 10. GUARDAR DATOS LIMPIOS
# ==================================================

datos.to_csv(
    ruta_salida,
    index=False
)


# ==================================================
# 11. MOSTRAR RESULTADOS
# ==================================================

print("\n======================================")
print("       LIMPIEZA TERMINADA")
print("======================================")

print(f"\nDatos limpios guardados en:")
print(ruta_salida)

print("\nPrimeras filas:")
print(datos.head())