# leer_sensor.py - lee la señal del sensor ultrasónico y grafica una ventana

import serial
import time
import matplotlib.pyplot as plt
import os

PUERTO = 'COM4'
BAUDIOS = 115200
N_MUESTRAS = 200

# Abrir puerto serial
ser = serial.Serial(PUERTO, BAUDIOS, timeout=1)

# Esperar a que Arduino se reinicie
time.sleep(2)

valores = []

print("Leyendo...")
print("Pasa la pieza frente al sensor ultrasónico")

while len(valores) < N_MUESTRAS:

    linea = ser.readline().decode('utf-8').strip()

    try:
        valor = float(linea)
    except ValueError:
        continue

    valores.append(valor)

    print(f"Muestra {len(valores)}: {valor:.2f} cm")

# Cerrar puerto
ser.close()

print(f"\nListas {len(valores)} muestras")


# ==================================================
# UBICAR LA CARPETA FIGURAS DEL PROYECTO
# ==================================================

carpeta_codigo = os.path.dirname(os.path.abspath(__file__))
carpeta_proyecto = os.path.dirname(carpeta_codigo)
carpeta_figuras = os.path.join(carpeta_proyecto, "figuras")

os.makedirs(carpeta_figuras, exist_ok=True)


# ==================================================
# CREAR NOMBRE DIFERENTE PARA CADA GRÁFICA
# ==================================================

numero = 1

while True:

    nombre = f"senal_ultrasonico_{numero:03d}.png"
    ruta_grafica = os.path.join(carpeta_figuras, nombre)

    # Si el archivo no existe, usamos ese número
    if not os.path.exists(ruta_grafica):
        break

    numero += 1


# ==================================================
# CREAR GRÁFICA
# ==================================================

plt.figure(figsize=(10, 5))

plt.plot(valores)

plt.title("Señal del sensor ultrasónico")
plt.xlabel("Muestra")
plt.ylabel("Distancia (cm)")

plt.grid(True)

# Guardar gráfica sin reemplazar las anteriores
plt.savefig(ruta_grafica)

# Mostrar gráfica
plt.show()

print("\nGráfica guardada correctamente:")
print(ruta_grafica)