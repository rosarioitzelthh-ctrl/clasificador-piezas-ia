# limpiar.py - limpia, corrige la linea base y normaliza los datos

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

os.makedirs(carpeta_figuras, exist_ok=True)


# ==================================================
# 2. LEER LOS DATOS
# ==================================================

if not os.path.exists(ruta_entrada):
    print("No se encontro datos.csv.")
    print("Primero ejecuta adquirir.py para capturar los datos.")
    exit()

datos = pd.read_csv(ruta_entrada)

print("======================================")
print("        LIMPIEZA DE DATOS")
print("======================================")

print("\nDatos originales:")
print(datos.head())


# ==================================================
# 3. MOSTRAR LAS CLASES
# ==================================================

clases_originales = datos['etiqueta'].dropna().unique()

print("\nClases encontradas:")

for clase in clases_originales:
    cantidad = datos[datos['etiqueta'] == clase]['ventana'].nunique()
    print(f"- {clase}: {cantidad} ventanas")


# ==================================================
# 4. QUITAR VALORES FUERA DEL RANGO FISICO
# ==================================================

# El HC-SR04 mide aproximadamente de 2 a 400 cm.
# Se eliminan valores menores o iguales a 0
# y valores mayores a 400 cm.

datos = datos[
    (datos['valor'] > 0) &
    (datos['valor'] <= 400)
].copy()

print("\nValores fuera del rango fisico eliminados.")


# ==================================================
# 5. APLICAR FILTRO DE MEDIA MOVIL
# ==================================================

# Se utiliza una media movil de 5 muestras.
# Se aplica por cada ventana para no mezclar
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
# 6. ELIMINAR NaN
# ==================================================

# El filtro deja algunos valores vacios
# al principio y al final de cada ventana.

datos = datos.dropna(
    subset=['valor_filtrado']
).copy()


# ==================================================
# 7. CALCULAR LA LINEA BASE
# ==================================================

# La linea base es el promedio de las primeras
# 20 muestras de cada ventana.

base = (
    datos[datos['t'] < 20]
    .groupby('ventana')['valor_filtrado']
    .mean()
)


print("\nLinea base de cada ventana:")
print(base)


# ==================================================
# 8. CALCULAR EL MOVIMIENTO DE LA LINEA BASE
# ==================================================

if len(base) >= 2:

    primera_ventana = base.index.min()
    ultima_ventana = base.index.max()

    movimiento_base = abs(
        base[ultima_ventana] - base[primera_ventana]
    )

    print(f"\nPrimera ventana: {primera_ventana}")
    print(f"Ultima ventana: {ultima_ventana}")
    print(
        f"Movimiento de la linea base: "
        f"{movimiento_base:.2f} cm"
    )

else:

    print("\nNo hay suficientes ventanas para calcular")
    print("el movimiento de la linea base.")


# ==================================================
# 9. CORREGIR LA LINEA BASE
# ==================================================

# A cada muestra se le resta la linea base
# correspondiente a su propia ventana.

datos['valor_corregido'] = (
    datos['valor_filtrado']
    - datos['ventana'].map(base)
)


# ==================================================
# 10. NORMALIZAR CON MIN-MAX
# ==================================================

# Cada ventana queda aproximadamente entre 0 y 1.

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
# 11. CREAR GRAFICAS POR CADA CLASE
# ==================================================

clases = datos['etiqueta'].dropna().unique()

print("\nGenerando graficas...")


for clase in clases:

    datos_clase = datos[
        datos['etiqueta'] == clase
    ]

    ventanas = datos_clase['ventana'].unique()

    if len(ventanas) < 2:
        print(
            f"No hay suficientes ventanas para "
            f"graficar {clase}."
        )
        continue

    # Primera y ultima ventana de esta clase
    ventana_inicial = ventanas[0]
    ventana_final = ventanas[-1]

    datos_inicial = datos[
        datos['ventana'] == ventana_inicial
    ]

    datos_final = datos[
        datos['ventana'] == ventana_final
    ]


    # ----------------------------------------------
    # GRAFICA
    # ----------------------------------------------

    plt.figure(figsize=(12, 7))


    # Primera ventana antes de limpiar
    plt.plot(
        datos_inicial['t'],
        datos_inicial['valor'],
        label=f'Inicial sin limpiar - ventana {ventana_inicial}'
    )


    # Ultima ventana antes de limpiar
    plt.plot(
        datos_final['t'],
        datos_final['valor'],
        label=f'Final sin limpiar - ventana {ventana_final}'
    )


    # Primera ventana despues de limpiar
    plt.plot(
        datos_inicial['t'],
        datos_inicial['valor_normalizado'],
        label=f'Inicial normalizada - ventana {ventana_inicial}'
    )


    # Ultima ventana despues de limpiar
    plt.plot(
        datos_final['t'],
        datos_final['valor_normalizado'],
        label=f'Final normalizada - ventana {ventana_final}'
    )


    plt.xlabel('Muestra')
    plt.ylabel('Valor')
    plt.title(
        f'Antes y despues de limpiar - {clase}'
    )

    plt.legend()
    plt.grid()


    # ----------------------------------------------
    # NOMBRE DE ARCHIVO
    # ----------------------------------------------

    nombre_clase = clase.replace(' ', '_')

    ruta_figura = os.path.join(
        carpeta_figuras,
        f'limpieza_{nombre_clase}.png'
    )


    plt.savefig(
        ruta_figura,
        dpi=300,
        bbox_inches='tight'
    )

    plt.close()


    print(
        f"Grafica creada: {ruta_figura}"
    )


# ==================================================
# 12. GRAFICA COMPARANDO LAS 3 CLASES
# ==================================================

plt.figure(figsize=(12, 7))


for clase in clases:

    datos_clase = datos[
        datos['etiqueta'] == clase
    ]

    ventanas = datos_clase['ventana'].unique()

    if len(ventanas) == 0:
        continue

    # Tomar la primera ventana de cada clase
    ventana = ventanas[0]

    datos_ventana = datos[
        datos['ventana'] == ventana
    ]

    plt.plot(
        datos_ventana['t'],
        datos_ventana['valor_normalizado'],
        label=f'{clase} - ventana {ventana}'
    )


plt.xlabel('Muestra')
plt.ylabel('Valor normalizado')

plt.title(
    'Comparacion de las tres clases despues de limpiar'
)

plt.legend()
plt.grid()


ruta_comparacion = os.path.join(
    carpeta_figuras,
    'comparacion_tres_clases.png'
)

plt.savefig(
    ruta_comparacion,
    dpi=300,
    bbox_inches='tight'
)

plt.close()


print(
    f"\nGrafica de las tres clases creada:"
)
print(ruta_comparacion)


# ==================================================
# 13. GUARDAR DATOS LIMPIOS
# ==================================================

datos.to_csv(
    ruta_salida,
    index=False
)


# ==================================================
# 14. RESULTADOS FINALES
# ==================================================

print("\n======================================")
print("       LIMPIEZA TERMINADA")
print("======================================")

print("\nDatos limpios guardados en:")
print(ruta_salida)

print("\nGraficas guardadas en:")
print(carpeta_figuras)

print("\nClases procesadas:")

for clase in clases:
    print(f"- {clase}")

print("\nProceso terminado correctamente.")