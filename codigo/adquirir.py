# adquirir.py - captura ventanas etiquetadas y las guarda en datos/datos.csv
import serial
import time
import csv

PUERTO = 'COM4'          # el tuyo puede ser otro: COM4, COM5...
BAUDIOS = 115200
N_MUESTRAS = 200          # largo de cada ventana
ARCHIVO = 'datos/datos.csv'

etiqueta = input("Etiqueta de esta pieza: ")
n_ventanas = int(input("Cuantas ventanas vas a capturar: "))

ser = serial.Serial(PUERTO, BAUDIOS, timeout=1)
time.sleep(2)             # el Arduino se reinicia al abrir el puerto

# 'a' = append: no borra lo que ya habias capturado antes
archivo = open(ARCHIVO, 'a', newline='')
escritor = csv.writer(archivo)

# TODO: si el archivo esta vacio, escribe primero la fila de encabezados
#       ventana,t,valor,etiqueta

# TODO: averigua en que numero de ventana te quedaste la vez pasada
#       pista: lee el CSV con pandas y toma el maximo de la columna 'ventana'
ventana = 0

for i in range(n_ventanas):
    input(f"\nVentana {ventana} ({etiqueta}). Enter y pasa la pieza...")
    ser.reset_input_buffer()          # tira lo que se acumulo mientras esperabas

    t = 0
    while t < N_MUESTRAS:
        linea = ser.readline().decode('utf-8').strip()
        try:
            valor = float(linea)
        except ValueError:
            continue
        escritor.writerow([ventana, t, valor, etiqueta])
        t += 1

    print(f"  {N_MUESTRAS} muestras guardadas")
    ventana += 1

archivo.close()
ser.close()
print(f"\nListo. Datos en {ARCHIVO}")