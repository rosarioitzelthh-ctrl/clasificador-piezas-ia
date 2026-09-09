# adquirir.py - captura ventanas etiquetadas y las guarda en datos/datos.csv

import serial
import time
import csv
import os
import pandas as pd


# ==================================================
# CONFIGURACIÓN
# ==================================================

PUERTO = 'COM4'
BAUDIOS = 115200

N_MUESTRAS = 200

ARCHIVO = 'datos/datos.csv'


# ==================================================
# CREAR CARPETA Y ARCHIVO SI NO EXISTEN
# ==================================================

os.makedirs('datos', exist_ok=True)

if not os.path.exists(ARCHIVO):
    with open(ARCHIVO, 'w', newline='') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(['ventana', 't', 'valor', 'etiqueta'])


# ==================================================
# SABER EN QUÉ VENTANA NOS QUEDAMOS
# ==================================================

try:
    datos_existentes = pd.read_csv(ARCHIVO)

    if len(datos_existentes) > 0:
        ventana = int(datos_existentes['ventana'].max()) + 1
    else:
        ventana = 0

except Exception:
    ventana = 0


print("======================================")
print("   ADQUISICIÓN DE DATOS - HC-SR04")
print("======================================")

print(f"\nSiguiente ventana: {ventana}")


# ==================================================
# DATOS DE LA CAPTURA
# ==================================================

etiqueta = input(
    "\nEtiqueta de esta pieza "
    "(tapado / mal_tapado / no_tapado): "
).strip().lower()

n_ventanas = int(
    input("Cuántas ventanas vas a capturar: ")
)


# ==================================================
# CONECTAR ARDUINO
# ==================================================

print(f"\nConectando con Arduino en {PUERTO}...")

ser = serial.Serial(
    PUERTO,
    BAUDIOS,
    timeout=1
)

time.sleep(2)

print("Arduino conectado correctamente.")


# ==================================================
# ABRIR CSV
# ==================================================

archivo = open(
    ARCHIVO,
    'a',
    newline=''
)

escritor = csv.writer(archivo)


# ==================================================
# CAPTURAR VENTANAS
# ==================================================

for i in range(n_ventanas):

    print("\n--------------------------------------")
    print(f"Ventana {ventana}")
    print(f"Etiqueta: {etiqueta}")
    print("--------------------------------------")

    input(
        "Coloca la pieza y presiona ENTER "
        "para comenzar la captura..."
    )

    # Eliminar datos viejos del puerto
    ser.reset_input_buffer()

    t = 0

    while t < N_MUESTRAS:

        linea = ser.readline().decode(
            'utf-8',
            errors='ignore'
        ).strip()

        try:
            valor = float(linea)

        except ValueError:
            continue

        # Guardar:
        # ventana, tiempo, distancia, etiqueta
        escritor.writerow([
            ventana,
            t,
            valor,
            etiqueta
        ])

        t += 1

    archivo.flush()

    print(
        f"✓ {N_MUESTRAS} muestras guardadas "
        f"para la ventana {ventana}"
    )

    ventana += 1


# ==================================================
# CERRAR TODO
# ==================================================

archivo.close()
ser.close()

print("\n======================================")
print("          CAPTURA TERMINADA")
print("======================================")

print(f"\nDatos guardados en:")
print(ARCHIVO)

print(f"\nÚltima ventana utilizada: {ventana - 1}")