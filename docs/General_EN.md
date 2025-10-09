# Technical Documentation — General (framework orchestrator)

The **General** class acts as an **orchestrator**: it receives a processed minimal dataset in `.csv` and sequentially runs the exploratory analysis, clustering, and results analysis stages.

> **Stack assumed in the examples:** `pandas`, `scipy`, `scikit-learn`, `matplotlib`

## Table of Contents
- [Overview](#overview)
- [Installation & prerequisites](#installation--prerequisites)
- [Flow of the execute method](#flow-of-the-execute-method)
- [Class API](#class-api)
- [Usage example](#usage-example)
- [Best practices](#best-practices)

## Overview
- Input: minimal dataset (`minimaldataset.csv`).
- Output: descriptive statistics, clusters, results analyses, charts, and a summary file (`<path>/<algorithm>_results.txt`).

## Installation & prerequisites
```bash
pip install pandas scipy scikit-learn matplotlib hdbscan
```

## Flow of the execute method
1. **ExploratoryAnalysis**
   - Loads dataset
   - Descriptive statistics
   - Normality test (Shapiro, Smirnov, or Anderson)
   - Spearman correlation matrix

2. **Clustering**
   - Runs the chosen algorithm:
     - KMeans → `k`
     - Agglomerative → `n_clusters`
     - Gaussian → `n_clusters`
     - HDBSCAN → `min_samples`, `min_cluster_size`
     - DBSCAN → `value_eps`, `value_minsamples`

3. **ResultsAnalysis**
   - Descriptive statistics by cluster
   - Significance tests
   - SRL profiles (tables and charts)
   - Exports results

---

## Class API
### `__init__(fileDataset, delimiterDataset, path)`
**Parameters:** `fileDataset, delimiterDataset, path`

**Example:**
```python
g.__init__(fileDataset, delimiterDataset, path)
```

### `execute(algorithm, fileGrade, delimiterGrade, normalityTeste)`
**Parameters:** `algorithm, fileGrade, delimiterGrade, normalityTeste`

**Example:**
```python
g.execute(algorithm, fileGrade, delimiterGrade, normalityTeste)
```


---

## Usage example
```python
from general import General

dataset = "out/minimaldataset.csv"

g = General(fileDataset=dataset, delimiterDataset=";", path="out/")

# Run with K-Means (k=3)
g.execute(
    algorithm="kmeans",
    normalityTeste="shapiro",
    k=3
)

# Run with HDBSCAN
g.execute(
    algorithm="hdbscan",
    min_samples=5,
    min_cluster_size=10
)

# Run with Agglomerative + grade file
g.execute(
    algorithm="agglomerative",
    n_clusters=3,
    fileGrade="out/grades.csv",
    delimiterGrade=";"
)
```

---

## Best practices
- Make sure `minimaldataset.csv` is ready before running the orchestrator.
- Check the **delimiter** (`;` or `,`) correctly.
- Keep separate directories in `path` to avoid overwriting results.
- Include expected columns: `iduser`, `time`, `SRL_Planning`, `SRL_Monitoring`, `SRL_Evaluation`, `TotalEvents`.
- For analyses with grades (`fileGrade`), validate consistency of the `iduser` column.
