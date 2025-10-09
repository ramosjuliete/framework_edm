# Technical Documentation — Clustering (with practical examples and simulated figures)

This class executes **clustering techniques** (e.g., K-Means, Hierarchical/Agglomerative, HDBSCAN) on educational data,
allowing you to find groups of students and interpret behavior patterns from dataset columns.


## Table of Contents
- [Overview](#overview)
- [Installation & prerequisites](#installation--prerequisites)
- [Recommended workflow](#recommended-workflow)
- [Class API](#class-api)
- [Practical examples (by method)](#practical-examples-by-method)
- [End-to-end example](#end-to-end-example)
- [Best practices and validation](#best-practices-and-validation)
- [Simulated figures](#simulated-figures)

## Overview
- **Input:** `DataFrame` with numeric columns.
- **Output:** cluster labels, quality metrics (silhouette, Dunn/DB), and files/figures when applicable.

## Installation & prerequisites
```bash
pip install pandas scikit-learn scipy matplotlib hdbscan
```

## Recommended workflow
1. Provide the minimal dataset ready for applying clustering algorithms.
2. Explore **K** via *Elbow* and **silhouette**, or the values for `min_samples` and `min_cluster_size`, and dendrograms to analyze the best parameter values.
3. Train the chosen algorithm (K-Means/Agglomerative/HDBSCAN).
4. Evaluate metrics and **interpret** the clusters (means per cluster).
5. Save results and figures.

---

## Class API
### `__init__(algorithm, path)`
**Parameters:** `algorithm, path`

**Example:**
```python
# Suppose real columns: iduser, time, SRL_Planning, SRL_Monitoring, SRL_Evaluation, TotalEvents
cl.__init__(algorithm, "out/")
```

### `removeIdentifierColumns(dataframe)`
**Parameters:** `dataframe`

**Example:**
```python
# Suppose real columns: iduser, time, SRL_Planning, SRL_Monitoring, SRL_Evaluation, TotalEvents
cl.removeIdentifierColumns(df)
```

### `dendogram_hdbscan(dataframe)`
**Parameters:** `dataframe`

**Example:**
```python
# Suppose real columns: iduser, time, SRL_Planning, SRL_Monitoring, SRL_Evaluation, TotalEvents
cl.dendogram_hdbscan(df)
```

### `analysisMeasuresHDBSCAN(dataframe, min_samples_values, min_cluster_size_values)`
**Parameters:** `dataframe, min_samples_values, min_cluster_size_values`

**Example:**
```python
# Suppose real columns: iduser, time, SRL_Planning, SRL_Monitoring, SRL_Evaluation, TotalEvents
# mim_samples_values and min_cluster_size_values are Python lists with several values for HDBSCAN parameters
cl.analysisMeasuresHDBSCAN(df, min_samples_values, min_cluster_size_values)
```

### `bestValueK_SilhouetteScores(dataframe)`
**Parameters:** `dataframe`

**Example:**
```python
# Suppose real columns: iduser, time, SRL_Planning, SRL_Monitoring, SRL_Evaluation, TotalEvents
cl.bestValueK_SilhouetteScores(df)
```

### `bestValueK_Elbow(dataframe)`
**Parameters:** `dataframe`

**Example:**
```python
# Suppose real columns: iduser, time, SRL_Planning, SRL_Monitoring, SRL_Evaluation, TotalEvents
cl.bestValueK_Elbow(df)
```

### `bestValueK_forAgglomerative(dataframe)`
**Parameters:** `dataframe`

**Example:**
```python
# Suppose real columns: iduser, time, SRL_Planning, SRL_Monitoring, SRL_Evaluation, TotalEvents
cl.bestValueK_forAgglomerative(df)
```

### `dunn_index(X, labels)`
**Parameters:** `X, labels`

**Example:**
```python
# Suppose real columns: iduser, time, SRL_Planning, SRL_Monitoring, SRL_Evaluation, TotalEvents
cl.dunn_index(X, labels)
```

### `internalValidation(labels, dataframe)`
**Parameters:** `labels, dataframe`

**Example:**
```python
# Suppose real columns: iduser, time, SRL_Planning, SRL_Monitoring, SRL_Evaluation, TotalEvents
cl.internalValidation(labels, df)
```

### `saveClustering(dataframe, name)`
**Parameters:** `dataframe, name`

**Example:**
```python
# Suppose real columns: iduser, time, SRL_Planning, SRL_Monitoring, SRL_Evaluation, TotalEvents
cl.saveClustering(df, name)
```

### `kmeans(dataframe, valueK)`
**Parameters:** `dataframe, valueK`

**Example:**
```python
# Suppose real columns: iduser, time, SRL_Planning, SRL_Monitoring, SRL_Evaluation, TotalEvents
cl.kmeans(df, 3)
```

### `agglomerative(dataframe, n_clusters)`
**Parameters:** `dataframe, n_clusters`

**Example:**
```python
# Suppose real columns: iduser, time, SRL_Planning, SRL_Monitoring, SRL_Evaluation, TotalEvents
cl.agglomerative(df, 3)
```

### `hdbscan(dataframe, value_min_samples, value_min_cluster_size)`
**Parameters:** `dataframe, value_min_samples, value_min_cluster_size`

**Example:**
```python
# Suppose real columns: iduser, time, SRL_Planning, SRL_Monitoring, SRL_Evaluation, TotalEvents
cl.hdbscan(df, value_min_samples, value_min_cluster_size)
```

### `dbscan(dataframe, value_eps, value_minsamples)`
**Parameters:** `dataframe, value_eps, value_minsamples`

**Example:**
```python
# Suppose real columns: iduser, time, SRL_Planning, SRL_Monitoring, SRL_Evaluation, TotalEvents
cl.dbscan(df, value_eps, value_minsamples)
```

### `gaussian(dataframe, n_clusters)`
**Parameters:** `dataframe, n_clusters`

**Example:**
```python
# Suppose real columns: iduser, time, SRL_Planning, SRL_Monitoring, SRL_Evaluation, TotalEvents
cl.gaussian(df, 3)
```


---

## Practical examples (by method)
```python
import pandas as pd
from clustering import Clustering

# Realistic DataFrame
df = pd.DataFrame({
    "iduser": [1,2,3,4,5,6,7,8,9,10],
    "time": [1200, 850, 930, 4000, 2100, 760, 1800, 3000, 2500, 1100],
    "SRL_Planning": [5,3,4,10,6,2,5,8,7,3],
    "SRL_Monitoring": [4,2,3,9,5,1,4,7,6,2],
    "SRL_Evaluation": [2,1,2,6,3,1,2,5,4,1],
    "TotalEvents": [80, 55, 61, 150, 98, 40, 77, 130, 115, 60]
})

cl = Clustering(algorithm="KMEANS", path="out/")

# 1) Best K via Silhouette
k_sil = cl.bestValueK_SilhouetteScores(df)

# 2) Best K via Elbow
k_elb = cl.bestValueK_Elbow(df)

# 3) K-Means with chosen K
labels = cl.kmeans(df, valueK=int(k_sil or 3))

# 4) Dendrogram (hierarchical clusters) 
# cl.hierarchical(df, method="ward", metric="euclidean")

# 5) HDBSCAN (when available)
# cl.hdbscan(df, min_cluster_size=5)

# 6) Additional metrics (Dunn/DB if implemented in the class)
# cl.dunn_index(df, labels)
# cl.davies_bouldin(df, labels)

# 7) Export clusters + summary
# cl.export_results(df, labels, path="out/")
```

---

## End-to-end example
```python
from clustering import Clustering
import pandas as pd

features = ["time","SRL_Planning","SRL_Monitoring","SRL_Evaluation","TotalEvents"]
df = ...  # your DataFrame with the above columns

cl = Clustering(algorithm="KMEANS", path="out/")

# 1) K exploration
k_sil = cl.bestValueK_SilhouetteScores(df[features])
k_elb = cl.bestValueK_Elbow(df[features])

# 2) Final training
k = int(k_sil or k_elb or 3)
labels = cl.kmeans(df[features], valueK=k)

# 3) Interpretation
df_clusters = df.copy()
df_clusters["cluster"] = labels
summary = df_clusters.groupby("cluster")[features].mean()
print(summary)
```

---

## Best practices and validation
- **Scaling**: standardize features before K-Means/Agglomerative.
- **Seeds/randomness**: set `random_state` for reproducibility (if the class allows it).
- **Sample size**: be careful with silhouette on very small datasets.
- **Balance**: check the number of items per cluster; use `min_cluster_size` in HDBSCAN when available.
- **Interpretation**: always generate a table with means per cluster and validate with domain experts.

---

## Simulated figures
> Below are **illustrative images (placeholders)** indicating what the method-generated charts would look like.
>
> - **Elbow Method**: `![Elbow](/mnt/data/plots_clustering_placeholders/elbow.png)`
> - **Silhouette Scores**: `![Silhouette](/mnt/data/plots_clustering_placeholders/silhouette.png)`
> - **Hierarchical Dendrogram**: `![Dendrogram](/mnt/data/plots_clustering_placeholders/dendrogram.png)`
> - **Cluster Scatter**: `![Scatter](/mnt/data/plots_clustering_placeholders/cluster_scatter.png)`
