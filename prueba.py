import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
from sklearn.metrics import davies_bouldin_score
import numpy as np

print("🎯 COMPROBACIÓN DE HIPÓTESIS: 3 CLUSTERS EN SESIONES DE COMPRADORES")
print("="*70)

# PASO 1: FORMALIZACIÓN Y PREPARACIÓN DE DATOS
print("\n📊 PASO 1: PREPARACIÓN DE DATOS")
print("-" * 40)

# Cargar el dataset
df = pd.read_csv('online_shoppers_intention.csv')

# 1. Seleccionar las features de la hipótesis
features = ['Administrative_Duration', 'Informational_Duration', 'ProductRelated_Duration']
X = df[features]

# Manejar nulos si los hubiera
X = X.fillna(0)

print(f"Variables seleccionadas: {features}")
print(f"Dimensiones de los datos: {X.shape}")

# 2. Escalar los datos (CRÍTICO)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print("✅ Datos escalados correctamente con StandardScaler")

# PASO 2: MODELADO (K-MEANS CLUSTERING)
print("\n🔍 PASO 2: CLUSTERING CON K-MEANS (K=3)")
print("-" * 45)

# Instanciamos K-Means con K=3 basado en la hipótesis
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)

# Entrenamos y obtenemos las etiquetas
labels = kmeans.fit_predict(X_scaled)

# Agregamos las etiquetas al DataFrame original para el análisis
df['cluster'] = labels

print(f"✅ Se generaron {len(df['cluster'].unique())} clusters")
print("\n📈 Distribución de sesiones por cluster:")
print(df['cluster'].value_counts().sort_index())

# PASO 3: VISUALIZACIÓN (t-SNE)
print("\n📊 PASO 3: VISUALIZACIÓN CON t-SNE")
print("-" * 35)

"""# 1. Aplicar t-SNE sobre los datos ESCALADOS
tsne = TSNE(n_components=2, perplexity=30, random_state=42)
tsne_results = tsne.fit_transform(X_scaled)

# 2. Crear un DataFrame para la visualización
df_tsne = pd.DataFrame()
df_tsne['tsne_1'] = tsne_results[:, 0]
df_tsne['tsne_2'] = tsne_results[:, 1]
df_tsne['cluster'] = labels

# 3. Graficar con Seaborn
plt.figure(figsize=(12, 8))
scatter = sns.scatterplot(
    x="tsne_1", y="tsne_2",
    hue="cluster",
    palette=sns.color_palette("hls", 3),
    data=df_tsne,
    legend="full",
    alpha=0.7,
    s=50
)
plt.title('Visualización t-SNE de los 3 Clusters de Sesiones', fontsize=14, fontweight='bold')
plt.xlabel('Componente t-SNE 1')
plt.ylabel('Componente t-SNE 2')
plt.legend(title='Cluster', loc='upper right')
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()"""

# PASO 4: VALIDACIÓN Y PERFILADO DE CLUSTERS
print("\n📈 PASO 4: VALIDACIÓN Y PERFILADO DE CLUSTERS")
print("-" * 50)

# 1. Validación Cuantitativa (Perfilado)
print("📋 PERFIL DE CLUSTERS (medias de duración en segundos):")
cluster_profile = df.groupby('cluster')[features].mean()
print(cluster_profile.round(2))

# 2. Validación de Métrica Interna
score_db = davies_bouldin_score(X_scaled, labels)
print(f"\n🎯 PUNTAJE DAVIES-BOULDIN: {score_db:.4f}")
print("   (Menor es mejor: clusters más densos y separados)")

# 3. Análisis de Revenue por cluster
if 'Revenue' in df.columns:
    print(f"\n💰 COMPORTAMIENTO DE COMPRA POR CLUSTER:")
    revenue_by_cluster = df.groupby('cluster')['Revenue'].mean()
    for cluster_id, tasa in revenue_by_cluster.items():
        print(f"   Cluster {cluster_id}: {tasa*100:.1f}% tasa de compra")

# INTERPRETACIÓN FINAL CON TUS HIPÓTESIS ESPECÍFICAS
print("\n" + "="*70)
print("🎯 INTERPRETACIÓN FINAL - VERIFICACIÓN DE HIPÓTESIS")
print("="*70)

# Analizar patrones de cada cluster según TUS hipótesis
for cluster_id in range(3):
    cluster_data = cluster_profile.loc[cluster_id]
    admin_dur = cluster_data['Administrative_Duration']
    info_dur = cluster_data['Informational_Duration']
    prod_dur = cluster_data['ProductRelated_Duration']
    
    print(f"\n🔍 CLUSTER {cluster_id} ({df[df['cluster'] == cluster_id].shape[0]} sesiones):")
    print(f"   • Administrative: {admin_dur:.0f}s")
    print(f"   • Informational: {info_dur:.0f}s") 
    print(f"   • ProductRelated: {prod_dur:.0f}s")
    
    def identificar_perfil_corregido(admin_dur, info_dur, prod_dur):

        # PERFIL 1: Product duration ALTO, otros dos BAJOS
        # "Bajos" = menos del 25% del tiempo de Producto
        if prod_dur > 1000 and admin_dur < (prod_dur * 0.25) and info_dur < (prod_dur * 0.25):
            return "PERFIL 1: Product-Focused (alto producto, bajos otros)"
        
        # PERFIL 2: Informacional > Admin y > Producto
        elif info_dur > admin_dur and info_dur > prod_dur:
            return "PERFIL 2: Investigador (info > admin > producto)"
        
        # PERFIL 3: Mucho tiempo en producto + admin + info  
        # Todos por encima de umbrales significativos
        elif prod_dur > 1000 and admin_dur > 200 and info_dur > 200:
            return "PERFIL 3: Alto Engagement (los 3 altos)"
        
        else:
            return "Perfil Mixto"

    print(identificar_perfil_corregido(admin_dur,info_dur,prod_dur))

# Aplica esta función y verás resultados más coherentes
# EVALUACIÓN FINAL DE COINCIDENCIA
print(f"\n💡 EVALUACIÓN FINAL DE LA HIPÓTESIS:")

# Contar cuántos clusters coinciden con tus perfiles
coincidencias = 0
perfiles_esperados = [
    "Product Duration ALTO, otros dos BAJOS",
    "Informacional > Admin y > Producto", 
    "Mucho tiempo en Producto + Admin + Info"
]

for cluster_id in range(3):
    cluster_data = cluster_profile.loc[cluster_id]
    admin_dur = cluster_data['Administrative_Duration']
    info_dur = cluster_data['Informational_Duration']
    prod_dur = cluster_data['ProductRelated_Duration']
    
    if (cluster_id == 0 and prod_dur > admin_dur and prod_dur > info_dur and admin_dur < info_dur) or \
       (cluster_id == 1 and info_dur > admin_dur and info_dur > prod_dur) or \
       (cluster_id == 2 and prod_dur > admin_dur and admin_dur > 100 and info_dur > 100):
        coincidencias += 1

if coincidencias == 3:
    print("   ✅ ¡HIPÓTESIS TOTALMENTE CONFIRMADA!")
    print("   Los 3 clusters coinciden exactamente con tus perfiles esperados")
elif coincidencias >= 2:
    print("   ⚠️  HIPÓTESIS PARCIALMENTE CONFIRMADA")
    print(f"   {coincidencias} de 3 clusters coinciden con tus perfiles")
else:
    print("   ❌ HIPÓTESIS NO CONFIRMADA")
    print("   Los clusters encontrados no coinciden con tus perfiles esperados")

print(f"\n📊 MÉTRICA DE CALIDAD: Davies-Bouldin = {score_db:.4f}")
if score_db < 1.0:
    print("   ✅ Excelente separación entre clusters")
elif score_db < 1.5:
    print("   ✅ Buena separación entre clusters") 
else:
    print("   ⚠️  Separación moderada entre clusters")

print(f"\n🎯 RECOMENDACIONES:")
print("   • Analizar si la asignación de clusters a perfiles es la correcta")
print("   • Considerar ajustar los umbrales de 'mucho tiempo' según los datos")
print("   • Validar con análisis de negocio (qué perfiles compran más)")

print(f"\n✅ ANÁLISIS COMPLETADO")