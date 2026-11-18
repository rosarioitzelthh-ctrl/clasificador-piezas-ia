
# clustering.py - agrupa los datos sin utilizar sus etiquetas

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import os

# Leer los datos
features = pd.read_csv('datos/features.csv')

# Separar las caracteristicas y las etiquetas
X = features.drop(columns=['ventana', 'etiqueta'])
y = features['etiqueta']

# Preparar los datos
X_esc = StandardScaler().fit_transform(X)

# Aplicar K-Means para encontrar 3 grupos
kmeans = KMeans(
    n_clusters=3,
    n_init=10,
    random_state=42
)

grupos = kmeans.fit_predict(X_esc)

# Mostrar la tabla que compara los grupos con las clases originales
print("\n========================================")
print("       RESULTADOS DE K-MEANS")
print("========================================")

tabla = pd.crosstab(
    y,
    grupos,
    rownames=['Clase original'],
    colnames=['Grupo encontrado']
)

print("\nTabla de comparacion:")
print(tabla)

# Aplicar PCA para representar los datos en dos dimensiones
pca = PCA(n_components=2)
componentes = pca.fit_transform(X_esc)

# Crear la grafica
plt.figure(figsize=(11, 8))

colores = ['royalblue', 'darkorange', 'forestgreen']

for grupo in sorted(set(grupos)):
    mascara = grupos == grupo

    plt.scatter(
        componentes[mascara, 0],
        componentes[mascara, 1],
        label=f'Grupo {grupo}',
        color=colores[grupo],
        s=65,
        alpha=0.75,
        edgecolors='black',
        linewidths=0.5
    )

# Agregar porcentajes y nombres
pc1 = pca.explained_variance_ratio_[0] * 100
pc2 = pca.explained_variance_ratio_[1] * 100

plt.xlabel(f'PC1 ({pc1:.2f}%)')
plt.ylabel(f'PC2 ({pc2:.2f}%)')
plt.title('Agrupamiento K-Means de los datos')

plt.legend(title='Grupos')
plt.grid(True, alpha=0.3)
plt.tight_layout()

# Guardar la grafica
os.makedirs('figuras', exist_ok=True)
plt.savefig(
    'figuras/clustering.png',
    dpi=300,
    bbox_inches='tight'
)

print("\nGrafica guardada en figuras/clustering.png")
print("\n========================================")
print("          FIN DEL ANALISIS")
print("========================================")

plt.show()
