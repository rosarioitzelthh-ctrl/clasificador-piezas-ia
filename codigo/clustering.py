
# clustering.py - K-Means y DBSCAN

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, DBSCAN
from sklearn.decomposition import PCA
import os

# ========================================
# LEER Y PREPARAR LOS DATOS
# ========================================

features = pd.read_csv('datos/features.csv')

X = features.drop(columns=['ventana', 'etiqueta'])
y = features['etiqueta']

escalador = StandardScaler()
X_esc = escalador.fit_transform(X)

os.makedirs('figuras', exist_ok=True)

# ========================================
# BLOQUE 1: K-MEANS
# ========================================

kmeans = KMeans(
    n_clusters=3,
    n_init=10,
    random_state=42
)

grupos = kmeans.fit_predict(X_esc)

print("\n========================================")
print("       RESULTADOS DE K-MEANS")
print("========================================")

tabla = pd.crosstab(
    y,
    grupos,
    rownames=['Clase original'],
    colnames=['Grupo encontrado']
)

print(tabla)

# PCA para representar los datos
pca = PCA(n_components=2)
componentes = pca.fit_transform(X_esc)

pc1 = pca.explained_variance_ratio_[0] * 100
pc2 = pca.explained_variance_ratio_[1] * 100

# Gráfica K-Means
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
        edgecolors='black'
    )

plt.xlabel(f'PC1 ({pc1:.2f}%)')
plt.ylabel(f'PC2 ({pc2:.2f}%)')
plt.title('Agrupamiento K-Means de los datos')
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig(
    'figuras/clustering_kmeans.png',
    dpi=300,
    bbox_inches='tight'
)

plt.show()

# ========================================
# BLOQUE 2: DBSCAN
# ========================================

print("\n========================================")
print("       RESULTADOS DE DBSCAN")
print("========================================")

valores_eps = [1.5, 2.0, 2.5, 3.0, 3.5, 4.0]

print("\nTabla de prueba:")
print("eps | Grupos encontrados | Puntos de ruido")

for eps in valores_eps:

    dbscan = DBSCAN(
        eps=eps,
        min_samples=5
    )

    grupos_db = dbscan.fit_predict(X_esc)

    n_grupos = len(set(grupos_db)) - (1 if -1 in grupos_db else 0)
    n_ruido = list(grupos_db).count(-1)

    print(f"{eps} | {n_grupos} | {n_ruido}")

# ========================================
# SELECCIONAR EPS
# ========================================

# Valor provisional. Se ajustará según la tabla obtenida.
eps_elegido = 2.5

dbscan = DBSCAN(
    eps=eps_elegido,
    min_samples=5
)

grupos_db = dbscan.fit_predict(X_esc)

n_grupos = len(set(grupos_db)) - (1 if -1 in grupos_db else 0)
n_ruido = list(grupos_db).count(-1)

print("\nResultados finales de DBSCAN:")
print("eps elegido:", eps_elegido)
print("Grupos encontrados:", n_grupos)
print("Puntos marcados como ruido:", n_ruido)

# ========================================
# GRAFICAR DBSCAN
# ========================================

plt.figure(figsize=(11, 8))

for grupo in sorted(set(grupos_db)):

    mascara = grupos_db == grupo

    if grupo == -1:
        plt.scatter(
            componentes[mascara, 0],
            componentes[mascara, 1],
            marker='x',
            color='red',
            s=120,
            linewidths=2,
            label='Ruido (-1)'
        )

    else:
        plt.scatter(
            componentes[mascara, 0],
            componentes[mascara, 1],
            s=65,
            alpha=0.75,
            edgecolors='black',
            label=f'Grupo {grupo}'
        )

plt.xlabel(f'PC1 ({pc1:.2f}%)')
plt.ylabel(f'PC2 ({pc2:.2f}%)')
plt.title(f'DBSCAN - eps={eps_elegido}, min_samples=5')
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig(
    'figuras/clustering.png',
    dpi=300,
    bbox_inches='tight'
)

plt.show()

print("\nGrafica DBSCAN guardada en figuras/clustering.png")

print("\n========================================")
print("          FIN DEL ANALISIS")
print("========================================")
