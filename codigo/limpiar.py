# limpiar.py - quita ruido y normaliza el dataset

import pandas as pd

# Cargar datos
datos = pd.read_csv('datos/datos.csv')

# Mostrar información inicial
print("Datos originales:")
print(datos.head())
print("Cantidad de datos:", len(datos))

# El KY-032 trabaja con señal digital.
# Normalmente sus valores son 0 y 1.
# Conservamos únicamente esos valores.
datos = datos[datos['valor'].isin([0, 1])].copy()

# Aplicar filtro de media móvil dentro de cada ventana
datos['valor_filtrado'] = (
    datos.groupby('ventana')['valor']
    .transform(lambda x: x.rolling(window=5, center=True).mean())
)

# Rellenar los NaN de las orillas usando el valor más cercano
datos['valor_filtrado'] = (
    datos.groupby('ventana')['valor_filtrado']
    .transform(lambda x: x.bfill().ffill())
)

# Guardar dataset limpio
datos.to_csv('datos/datos_limpios.csv', index=False)

print("Datos limpios guardados correctamente.")
print("Cantidad de datos finales:", len(datos))