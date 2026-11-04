
# control.py - Bucle de control completo
# Semana 8 - Arduino y Python

import serial
import time
import os
import numpy as np
import pandas as pd
import joblib

# ==========================================
# CONFIGURACION
# ==========================================

PUERTO = 'COM4'
BAUDIOS = 115200
N_MUESTRAS = 200

FS = 100.0
UMBRAL = 5

# ==========================================
# UBICAR Y CARGAR EL MODELO
# ==========================================

carpeta_codigo = os.path.dirname(os.path.abspath(__file__))
carpeta_proyecto = os.path.dirname(carpeta_codigo)

ruta_modelo = os.path.join(
    carpeta_proyecto, 'modelo.pkl'
)

paquete = joblib.load(ruta_modelo)

modelo = paquete['modelo']
escalador = paquete['escalador']
columnas = paquete['columnas']

# ==========================================
# 1. CAPTURAR VENTANA
# ==========================================

def capturar_ventana(ser, n):

    muestras = []

    while len(muestras) < n:

        linea = ser.readline().decode(
            'utf-8', errors='ignore'
        ).strip()

        try:
            valor = float(linea)

            muestras.append(valor)

        except ValueError:
            continue

    return np.array(muestras)


# ==========================================
# 2. LIMPIAR VENTANA
# ==========================================

def limpiar(ventana):

    datos = pd.Series(ventana)

    # Eliminar valores fuera del rango
    datos = datos[
        (datos > 0) & (datos <= 400)
    ]

    # Aplicar media movil de 5 muestras
    filtrado = datos.rolling(
        window=5,
        center=True
    ).mean()

    # Conservar las mismas filas que
    # sobreviven al proceso de limpiar.py
    datos_limpios = datos[filtrado.notna()]

    return datos_limpios.to_numpy()


# ==========================================
# 3. CALCULAR CARACTERISTICAS
# ==========================================

def calcular_features(ventana):

    x = np.asarray(ventana, dtype=float)

    if len(x) < 2:
        raise ValueError("Ventana insuficiente")

    # Caracteristicas de tiempo
    media = x.mean()
    desv = x.std()
    minimo = x.min()
    maximo = x.max()
    rango = maximo - minimo
    energia = np.sum(x ** 2)
    duracion = np.sum(np.abs(x) > UMBRAL)

    # Transformada de Fourier
    espectro = np.abs(np.fft.rfft(x))[1:]

    frecuencias = np.fft.rfftfreq(
        len(x), 1 / FS
    )[1:]

    # Frecuencia dominante
    if len(espectro) > 0:
        f_dominante = frecuencias[
            np.argmax(espectro)
        ]
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

    # Bandas de frecuencia
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

    return {
        'media': media,
        'desv': desv,
        'minimo': minimo,
        'maximo': maximo,
        'rango': rango,
        'energia': energia,
        'duracion': duracion,
        'f_dominante': f_dominante,
        'centroide': centroide,
        'energia_espectral': energia_espectral,
        'banda_baja': banda_baja,
        'banda_media': banda_media,
        'banda_alta': banda_alta
    }


# ==========================================
# ORDENES PARA ARDUINO
# ==========================================

ordenes = {
    'tapado': b'A',
    'mal_tapado': b'B',
    'no_tapado': b'C'
}


# ==========================================
# CONECTAR CON ARDUINO
# ==========================================

print("======================================")
print("       SISTEMA DE CLASIFICACION")
print("======================================")

ser = serial.Serial(
    PUERTO,
    BAUDIOS,
    timeout=1
)

time.sleep(2)

print("Arduino conectado.")
print("Sistema en funcionamiento.")
print("Presiona Ctrl+C para detener.")


# ==========================================
# BUCLE PRINCIPAL
# ==========================================

try:

    while True:

        print("\nCapturando pieza...")

        # 1. Capturar
        ventana = capturar_ventana(
            ser, N_MUESTRAS
        )

        # 2. Limpiar
        ventana = limpiar(ventana)

        if len(ventana) < 2:
            print("Lecturas insuficientes.")
            ser.write(b'0')
            continue

        # 3. Calcular caracteristicas
        f = calcular_features(ventana)

        X = pd.DataFrame([f])[columnas]

        # 4. Clasificar
        X_esc = escalador.transform(X)

        etiqueta = modelo.predict(X_esc)[0]

        # 5. Enviar orden
        if etiqueta in ordenes:

            ser.write(ordenes[etiqueta])
            ser.flush()

            print("Clasificacion:", etiqueta)
            print("Orden enviada:", ordenes[etiqueta].decode())

            time.sleep(0.5)

            # Regresar a reposo
            ser.write(b'0')
            ser.flush()

        else:

            print("Clase desconocida:", etiqueta)
            ser.write(b'0')

except KeyboardInterrupt:

    print("\nSistema detenido.")

finally:

    ser.write(b'0')
    ser.close()

    print("Puerto serial cerrado.")
