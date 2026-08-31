# leer_sensor.py - lee la señal del sensor y grafica una ventana
import serial
import time
import matplotlib.pyplot as plt

PUERTO = 'COM3'          # el tuyo puede ser otro: COM4, COM5...
BAUDIOS = 115200
N_MUESTRAS = 200          # con delay(10) son unos 2 segundos

ser = serial.Serial(PUERTO, BAUDIOS, timeout=1)
time.sleep(2)             # el Arduino se reinicia al abrir el puerto

valores = []
print("Leyendo... pasa la pieza frente al sensor")

while len(valores) < N_MUESTRAS:
    linea = ser.readline().decode('utf-8').strip()
    try:
        valor = float(linea)
    except ValueError:
        continue          # linea incompleta, la saltamos
    valores.append(valor)
    print(valor)          # para ver la señal en vivo

ser.close()
print(f"Listas {len(valores)} muestras")

# TODO: graficar 'valores' con matplotlib
# pista: plt.plot(), etiqueta los ejes (muestra y valor del sensor)
#        y guarda la figura en '../figuras/senal.png'