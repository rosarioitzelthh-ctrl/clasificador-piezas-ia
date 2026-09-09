# limpiar.py - quita ruido y normaliza el dataset
import pandas as pd

datos = pd.read_csv('datos/datos.csv')

# ==================================================
# 1. QUITAR VALORES FUERA DEL RANGO FÍSICO
# ==================================================

# El HC-SR04 mide distancia en centímetros.
# Se eliminan valores menores o iguales a 0
# y valores mayores a 400 cm.

datos = datos[
    (datos['valor'] > 0) &
    (datos['valor'] <= 400)
].copy()


# ==================================================
# 2. APLICAR FILTRO DE MEDIA MÓVIL
# ==================================================

# Se utiliza una media móvil de 5 muestras.
# El filtro se aplica por cada ventana para no
# mezclar los datos de diferentes piezas.

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
# 3. QUITAR LOS NaN
# ==================================================

# La media móvil deja algunos valores vacíos
# al principio y al final de cada ventana.
# Se eliminan esos valores.

datos = datos.dropna(
    subset=['valor_filtrado']
).copy()


# ==================================================
# 4. NORMALIZAR
# ==================================================

# Se llevan los valores a una escala de 0 a 1
# dentro de cada ventana.

datos['valor_normalizado'] = (
    datos.groupby('ventana')['valor_filtrado']
    .transform(
        lambda x:
        (x - x.min()) / (x.max() - x.min())
        if x.max() != x.min()
        else 0
    )
)


# ==================================================
# 5. GUARDAR DATOS LIMPIOS
# ==================================================

datos.to_csv(
    'datos/datos_limpios.csv',
    index=False
)

print("Limpieza terminada.")
print("Archivo guardado en: datos/datos_limpios.csv")