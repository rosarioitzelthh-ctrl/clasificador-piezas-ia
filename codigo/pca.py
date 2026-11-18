
# pca.py - reduce las caracteristicas a dos componentes y las grafica

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import os

# Leer los datos
features = pd.read_csv('datos/features.csv')

# Separar las caracteristicas y las etiquetas
X = features.drop(columns=['ventana', 'etiqueta'])
y = features['etiqueta']

# Estandarizar los datos
X_esc = StandardScaler().fit_transform(X)

# Aplicar PCA para obtener dos componentes
pca = PCA(n_components=2)
componentes = pca.fit_transform(X_esc)

# Mostrar los porcentajes de varianza
pc1 = pca.explained_variance_ratio_[0] * 100
pc2 = pca.explained_variance_ratio_[1] * 100
total = pc1 + pc2

print("\n--- RESULTADOS DEL PCA ---")
print(f"PC1: {pc1:.2f}%")
print(f"PC2: {pc2:.2f}%")
print(f"Varianza acumulada: {total:.2f}%")


# Crear la grafica PCA
plt.figure(figsize=(11, 8))

colores = {
    'tapado': 'royalblue',
    'mal_tapado': 'darkorange',
    'no_tapado': 'forestgreen'
}

for etiqueta in y.unique():
    mascara = y == etiqueta

    plt.scatter(
        componentes[mascara, 0],
        componentes[mascara, 1],
        label=etiqueta,
        color=colores[etiqueta],
        s=65,
        alpha=0.75,
        edgecolors='black',
        linewidths=0.5
    )

# Porcentajes
pc1 = pca.explained_variance_ratio_[0] * 100
pc2 = pca.explained_variance_ratio_[1] * 100

plt.xlabel(f'PC1 ({pc1:.2f}%)')
plt.ylabel(f'PC2 ({pc2:.2f}%)')
plt.title('Analisis PCA de las tres clases')

plt.legend(title='Clases')
plt.grid(True, alpha=0.3)

plt.tight_layout()

# Guardar grafica
os.makedirs('figuras', exist_ok=True)
plt.savefig('figuras/pca.png', dpi=300, bbox_inches='tight')

# Agregar nombres a los ejes
plt.xlabel(f'PC1 ({pc1:.2f}%)')
plt.ylabel(f'PC2 ({pc2:.2f}%)')
plt.title('Analisis PCA de las tres clases')
plt.legend(title='Clases')
plt.grid(True)

# Guardar la grafica
os.makedirs('figuras', exist_ok=True)
plt.savefig('figuras/pca.png', dpi=300, bbox_inches='tight')

print("\nGrafica guardada en figuras/pca.png")

# Buscar los puntos mas alejados del centro
distancias = (componentes[:, 0]**2 + componentes[:, 1]**2)**0.5

indices = distancias.argsort()[-5:][::-1]

print("\n--- VENTANAS MAS ALEJADAS ---")

for i in indices:
    print(
        f"Ventana: {features.iloc[i]['ventana']} | "
        f"Clase: {y.iloc[i]} | "
        f"PC1: {componentes[i, 0]:.2f} | "
        f"PC2: {componentes[i, 1]:.2f} | "
        f"Distancia: {distancias[i]:.2f}"
    )

plt.show()
