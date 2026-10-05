
# entrenar.py
# Entrena el clasificador y guarda el modelo

import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier

from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    ConfusionMatrixDisplay
)

import matplotlib.pyplot as plt
import os


# ======================================
# RUTAS
# ======================================

carpeta_codigo = os.path.dirname(os.path.abspath(__file__))
carpeta_proyecto = os.path.dirname(carpeta_codigo)

ruta_datos = os.path.join(
    carpeta_proyecto,
    'datos',
    'features.csv'
)

ruta_modelo = os.path.join(
    carpeta_proyecto,
    'modelo.pkl'
)

carpeta_figuras = os.path.join(
    carpeta_proyecto,
    'figuras'
)

os.makedirs(carpeta_figuras, exist_ok=True)


# ======================================
# LEER LOS DATOS
# ======================================

features = pd.read_csv(ruta_datos)


# ======================================
# SEPARAR CARACTERISTICAS Y ETIQUETAS
# ======================================

X = features.drop(
    columns=['ventana', 'etiqueta']
)

y = features['etiqueta']


# ======================================
# SEPARAR DATOS PARA ENTRENAR Y PROBAR
# ======================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    stratify=y,
    random_state=42
)


print("======================================")
print("       DATOS PARA ENTRENAMIENTO")
print("======================================")

print(f"Ejemplos para aprender: {len(X_train)}")
print(f"Ejemplos para probar: {len(X_test)}")


# ======================================
# PREPARAR LOS DATOS
# ======================================

escalador = StandardScaler()

X_train_esc = escalador.fit_transform(X_train)

X_test_esc = escalador.transform(X_test)


# ======================================
# CREAR Y ENTRENAR EL MODELO
# ======================================

modelo = KNeighborsClassifier(
    n_neighbors=5
)

modelo.fit(
    X_train_esc,
    y_train
)


# ======================================
# HACER PREDICCIONES
# ======================================

y_pred = modelo.predict(
    X_test_esc
)


# ======================================
# CALCULAR EXACTITUD
# ======================================

exactitud = accuracy_score(
    y_test,
    y_pred
)

print("\n======================================")
print("             RESULTADOS")
print("======================================")

print(f"\nExactitud: {exactitud:.4f}")


# ======================================
# MATRIZ DE CONFUSION
# ======================================

clases = sorted(y.unique())

matriz = confusion_matrix(
    y_test,
    y_pred,
    labels=clases
)

print("\nMatriz de confusion:")
print(matriz)

print("\nClases en ese orden:")
print(clases)


# ======================================
# GRAFICA DE LA MATRIZ
# ======================================

disp = ConfusionMatrixDisplay(
    confusion_matrix=matriz,
    display_labels=clases
)

disp.plot()

plt.title("Matriz de confusion")

plt.savefig(
    os.path.join(
        carpeta_figuras,
        'confusion.png'
    ),
    dpi=300,
    bbox_inches='tight'
)

plt.close()


print("\nGrafica guardada en:")
print(
    os.path.join(
        carpeta_figuras,
        'confusion.png'
    )
)


# ======================================
# GUARDAR MODELO, ESCALADOR Y COLUMNAS
# ======================================

joblib.dump(
    {
        'modelo': modelo,
        'escalador': escalador,
        'columnas': list(X.columns)
    },
    ruta_modelo
)


print("\nModelo guardado en:")
print(ruta_modelo)


# ======================================
# FINAL
# ======================================

print("\n======================================")
print("       ENTRENAMIENTO TERMINADO")
print("======================================")
