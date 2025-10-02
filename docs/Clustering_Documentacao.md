# Documentação Técnica — Clustering (com exemplos práticos e figuras simuladas)

Esta classe executa **técnicas de clusterização** (p.ex.: K-Means, Hierárquico/Aglomerativo, HDBSCAN) sobre dados educacionais,
permitindo encontrar grupos de estudantes e interpretar padrões de comportamento a partir de colunas do dataset.


## Sumário
- [Visão geral](#visão-geral)
- [Instalação e pré-requisitos](#instalação-e-pré-requisitos)
- [Fluxo recomendado](#fluxo-recomendado)
- [API da classe](#api-da-classe)
- [Exemplos práticos (por método)](#exemplos-práticos-por-método)
- [Exemplo ponta-a-ponta](#exemplo-ponta-a-ponta)
- [Boas práticas e validação](#boas-práticas-e-validação)
- [Figuras simuladas](#figuras-simuladas)

## Visão geral
- **Entrada:** `DataFrame` com colunas numéricas.
- **Saída:** labels de cluster, métricas de qualidade (silhueta, Dunn/DB), e arquivos/figuras quando aplicável.

## Instalação e pré-requisitos
```bash
pip install pandas scikit-learn scipy matplotlib hdbscan
```

## Fluxo recomendado
1. Enviar o dataset minimal pronto para aplicação de algoritmos de agrupamento.
2. Explorar **K** via *Elbow* e **silhueta** ou os valores min_samples e min_cluster_size e dendogramas para analisar os melhores valores de parâmetros.
3. Treinar o algoritmo escolhido (K-Means/Hierárquico/HDBSCAN).
4. Avaliar métricas e **interpretar** os clusters (médias por cluster).
5. Salvar resultados e figuras.

---

## API da classe
### `__init__(algorithm, path)`
**Parâmetros:** `algorithm, path`

**Exemplo:**
```python
# Suponha colunas reais: iduser, time, SRL_Planning, SRL_Monitoring, SRL_Evaluation, TotalEvents
cl.__init__(algorithm, "out/")
```

### `removeIdentifierColumns(dataframe)`
**Parâmetros:** `dataframe`

**Exemplo:**
```python
# Suponha colunas reais: iduser, time, SRL_Planning, SRL_Monitoring, SRL_Evaluation, TotalEvents
cl.removeIdentifierColumns(df)
```

### `dendogram_hdbscan(dataframe)`
**Parâmetros:** `dataframe`

**Exemplo:**
```python
# Suponha colunas reais: iduser, time, SRL_Planning, SRL_Monitoring, SRL_Evaluation, TotalEvents
cl.dendogram_hdbscan(df)
```

### `analysisMeasuresHDBSCAN(dataframe, min_samples_values, min_cluster_size_values)`
**Parâmetros:** `dataframe, min_samples_values, min_cluster_size_values`

**Exemplo:**
```python
# Suponha colunas reais: iduser, time, SRL_Planning, SRL_Monitoring, SRL_Evaluation, TotalEvents
# mim_samples_values e min_cluster_size_values são listas em python com diversos valores para os parâmetros do HDBSCAN
cl.analysisMeasuresHDBSCAN(df, min_samples_values, min_cluster_size_values)
```

### `bestValueK_SilhouetteScores(dataframe)`
**Parâmetros:** `dataframe`

**Exemplo:**
```python
# Suponha colunas reais: iduser, time, SRL_Planning, SRL_Monitoring, SRL_Evaluation, TotalEvents
cl.bestValueK_SilhouetteScores(df)
```

### `bestValueK_Elbow(dataframe)`
**Parâmetros:** `dataframe`

**Exemplo:**
```python
# Suponha colunas reais: iduser, time, SRL_Planning, SRL_Monitoring, SRL_Evaluation, TotalEvents
cl.bestValueK_Elbow(df)
```

### `bestValueK_forAgglomerative(dataframe)`
**Parâmetros:** `dataframe`

**Exemplo:**
```python
# Suponha colunas reais: iduser, time, SRL_Planning, SRL_Monitoring, SRL_Evaluation, TotalEvents
cl.bestValueK_forAgglomerative(df)
```

### `dunn_index(X, labels)`
**Parâmetros:** `X, labels`

**Exemplo:**
```python
# Suponha colunas reais: iduser, time, SRL_Planning, SRL_Monitoring, SRL_Evaluation, TotalEvents
cl.dunn_index(X, labels)
```

### `internalValidation(labels, dataframe)`
**Parâmetros:** `labels, dataframe`

**Exemplo:**
```python
# Suponha colunas reais: iduser, time, SRL_Planning, SRL_Monitoring, SRL_Evaluation, TotalEvents
cl.internalValidation(labels, df)
```

### `saveClustering(dataframe, name)`
**Parâmetros:** `dataframe, name`

**Exemplo:**
```python
# Suponha colunas reais: iduser, time, SRL_Planning, SRL_Monitoring, SRL_Evaluation, TotalEvents
cl.saveClustering(df, name)
```

### `kmeans(dataframe, valueK)`
**Parâmetros:** `dataframe, valueK`

**Exemplo:**
```python
# Suponha colunas reais: iduser, time, SRL_Planning, SRL_Monitoring, SRL_Evaluation, TotalEvents
cl.kmeans(df, 3)
```

### `agglomerative(dataframe, n_clusters)`
**Parâmetros:** `dataframe, n_clusters`

**Exemplo:**
```python
# Suponha colunas reais: iduser, time, SRL_Planning, SRL_Monitoring, SRL_Evaluation, TotalEvents
cl.agglomerative(df, 3)
```

### `hdbscan(dataframe, value_min_samples, value_min_cluster_size)`
**Parâmetros:** `dataframe, value_min_samples, value_min_cluster_size`

**Exemplo:**
```python
# Suponha colunas reais: iduser, time, SRL_Planning, SRL_Monitoring, SRL_Evaluation, TotalEvents
cl.hdbscan(df, value_min_samples, value_min_cluster_size)
```

### `dbscan(dataframe, value_eps, value_minsamples)`
**Parâmetros:** `dataframe, value_eps, value_minsamples`

**Exemplo:**
```python
# Suponha colunas reais: iduser, time, SRL_Planning, SRL_Monitoring, SRL_Evaluation, TotalEvents
cl.dbscan(df, value_eps, value_minsamples)
```

### `gaussian(dataframe, n_clusters)`
**Parâmetros:** `dataframe, n_clusters`

**Exemplo:**
```python
# Suponha colunas reais: iduser, time, SRL_Planning, SRL_Monitoring, SRL_Evaluation, TotalEvents
cl.gaussian(df, 3)
```


---

## Exemplos práticos (por método)
```python
import pandas as pd
from clustering import Clustering

# DataFrame realista
df = pd.DataFrame({
    "iduser": [1,2,3,4,5,6,7,8,9,10],
    "time": [1200, 850, 930, 4000, 2100, 760, 1800, 3000, 2500, 1100],
    "SRL_Planning": [5,3,4,10,6,2,5,8,7,3],
    "SRL_Monitoring": [4,2,3,9,5,1,4,7,6,2],
    "SRL_Evaluation": [2,1,2,6,3,1,2,5,4,1],
    "TotalEvents": [80, 55, 61, 150, 98, 40, 77, 130, 115, 60]
})

cl = Clustering(algorithm="KMEANS", path="out/")

# 1) Melhor K via Silhueta
k_sil = cl.bestValueK_SilhouetteScores(df)

# 2) Melhor K via Elbow
k_elb = cl.bestValueK_Elbow(df)

# 3) K-Means com K escolhido
labels = cl.kmeans(df, valueK=int(k_sil or 3))

# 4) Dendrograma (clusters hierárquicos) 
# cl.hierarchical(df, method="ward", metric="euclidean")

# 5) HDBSCAN (quando disponível)
# cl.hdbscan(df, min_cluster_size=5)

# 6) Métricas adicionais (Dunn/DB se implementadas na classe)
# cl.dunn_index(df, labels)
# cl.davies_bouldin(df, labels)

# 7) Exportar clusters + resumo
# cl.export_results(df, labels, path="out/")
```

---

## Exemplo ponta-a-ponta
```python
from clustering import Clustering
import pandas as pd

features = ["time","SRL_Planning","SRL_Monitoring","SRL_Evaluation","TotalEvents"]
df = ...  # seu DataFrame com as colunas acima

cl = Clustering(algorithm="KMEANS", path="out/")

# 1) Exploração de K
k_sil = cl.bestValueK_SilhouetteScores(df[features])
k_elb = cl.bestValueK_Elbow(df[features])

# 2) Treino final
k = int(k_sil or k_elb or 3)
labels = cl.kmeans(df[features], valueK=k)

# 3) Interpretação
df_clusters = df.copy()
df_clusters["cluster"] = labels
summary = df_clusters.groupby("cluster")[features].mean()
print(summary)
```

---

## Boas práticas e validação
- **Escalonamento**: padronize as features antes de K-Means/Agglomerativo.
- **Sementes/aleatoriedade**: defina `random_state` para reprodutibilidade (se a classe permitir).
- **Tamanho de amostra**: cuidado com silhueta em bases muito pequenas.
- **Balanceamento**: verifique o número de itens por cluster; use `min_cluster_size` no HDBSCAN quando disponível.
- **Interpretação**: sempre gere uma tabela com médias por cluster e valide com especialistas do domínio.

---

## Figuras simuladas
> Abaixo, **imagens ilustrativas (placeholders)** indicando como seriam os gráficos gerados pelos métodos.
>
> - **Elbow Method**: `![Elbow](/mnt/data/plots_clustering_placeholders/elbow.png)`
> - **Silhouette Scores**: `![Silhouette](/mnt/data/plots_clustering_placeholders/silhouette.png)`
> - **Hierarchical Dendrogram**: `![Dendrogram](/mnt/data/plots_clustering_placeholders/dendrogram.png)`
> - **Cluster Scatter**: `![Scatter](/mnt/data/plots_clustering_placeholders/cluster_scatter.png)`
