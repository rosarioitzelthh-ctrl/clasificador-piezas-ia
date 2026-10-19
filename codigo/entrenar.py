# entrenar.py
# Compara K-NN con dos redes neuronales

import os
import warnings
import joblib
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay

warnings.filterwarnings("ignore", category=UserWarning)

# ======================================
# RUTAS
# ======================================

carpeta_codigo = os.path.dirname(os.path.abspath(__file__))
carpeta_proyecto = os.path.dirname(carpeta_codigo)

ruta_datos = os.path.join(
    carpeta_proyecto, "datos", "features.csv"
)

ruta_modelo = os.path.join(
    carpeta_proyecto, "modelo.pkl"
)

ruta_comparacion = os.path.join(
    carpeta_proyecto, "datos", "comparacion_modelos.csv"
)

carpeta_figuras = os.path.join(carpeta_proyecto, "figuras")
os.makedirs(carpeta_figuras, exist_ok=True)

# ======================================
# LEER LOS DATOS
# ======================================

print("Leyendo los datos...")

features = pd.read_csv(ruta_datos)

X = features.drop(columns=["ventana", "etiqueta"])
y = features["etiqueta"]

print(f"Total de ejemplos: {len(features)}")
print("\nEjemplos por clase:")
print(y.value_counts())

# ======================================
# SEPARAR LOS DATOS
# ======================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    stratify=y,
    random_state=42
)

print("\nDatos para aprender:", len(X_train))
print("Datos para probar:", len(X_test))

# ======================================
# PREPARAR LOS DATOS
# ======================================

escalador = StandardScaler()

X_train_esc = escalador.fit_transform(X_train)
X_test_esc = escalador.transform(X_test)

# ======================================
# CREAR LOS TRES MODELOS
# ======================================

modelos = {
    "K-NN semana 7": KNeighborsClassifier(
        n_neighbors=5
    ),

    "Red de 10 neuronas": MLPClassifier(
        hidden_layer_sizes=(10,),
        max_iter=2000,
        random_state=42
    ),

    "Red de 50 neuronas": MLPClassifier(
        hidden_layer_sizes=(50,),
        max_iter=2000,
        random_state=42
    )
}

# ======================================
# ENTRENAR Y COMPARAR
# ======================================

resultados = {}

print("\n======================================")
print("       COMPARACION DE MODELOS")
print("======================================")

for nombre, modelo in modelos.items():

    print(f"\nEntrenando: {nombre}...")

    modelo.fit(X_train_esc, y_train)

    pred_train = modelo.predict(X_train_esc)
    pred_test = modelo.predict(X_test_esc)

    exactitud_train = accuracy_score(y_train, pred_train)
    exactitud_test = accuracy_score(y_test, pred_test)

    resultados[nombre] = {
        "Exactitud train": exactitud_train,
        "Exactitud test": exactitud_test
    }

    print(f"Exactitud train: {exactitud_train:.4f} "
          f"({exactitud_train * 100:.2f}%)")

    print(f"Exactitud test:  {exactitud_test:.4f} "
          f"({exactitud_test * 100:.2f}%)")

# ======================================
# MOSTRAR Y GUARDAR LA TABLA
# ======================================

tabla = pd.DataFrame(resultados).T
tabla.index.name = "Modelo"

print("\n======================================")
print("          TABLA DE RESULTADOS")
print("======================================")
print(tabla.round(4))

tabla.to_csv(ruta_comparacion, encoding="utf-8-sig")

print("\nTabla guardada en:")
print(ruta_comparacion)

# ======================================
# GUARDAR GRAFICA DE COMPARACION
# ======================================

tabla.plot(kind="bar", figsize=(9, 5))

plt.title("Comparacion de los modelos")
plt.ylabel("Exactitud")
plt.xlabel("Modelo")
plt.ylim(0, 1.05)
plt.xticks(rotation=15, ha="right")
plt.legend(["Entrenamiento", "Prueba"])
plt.tight_layout()

ruta_grafica = os.path.join(
    carpeta_figuras, "comparacion_modelos.png"
)

plt.savefig(ruta_grafica, dpi=300, bbox_inches="tight")
plt.close()

print("\nGrafica guardada en:")
print(ruta_grafica)

# ======================================
# MATRIZ DE CONFUSION DEL K-NN
# ======================================

modelo_knn = modelos["K-NN semana 7"]
pred_knn = modelo_knn.predict(X_test_esc)
clases = sorted(y.unique())

matriz = confusion_matrix(
    y_test, pred_knn, labels=clases
)

disp = ConfusionMatrixDisplay(
    confusion_matrix=matriz,
    display_labels=clases
)

disp.plot()
plt.title("Matriz de confusion - K-NN")
plt.tight_layout()

ruta_confusion = os.path.join(
    carpeta_figuras, "confusion.png"
)

plt.savefig(ruta_confusion, dpi=300, bbox_inches="tight")
plt.close()

# ======================================
# CONSERVAR EL MODELO DE LA SEMANA 7
# ======================================

# Por ahora mantenemos K-NN como modelo principal.
# Elegiremos si conviene cambiarlo despues de revisar
# los resultados de los tres modelos.

joblib.dump(
    {
        "modelo": modelo_knn,
        "escalador": escalador,
        "columnas": list(X.columns)
    },
    ruta_modelo
)

print("\nModelo K-NN guardado en:")
print(ruta_modelo)

print("\n======================================")
print("       COMPARACION TERMINADA")
print("======================================")