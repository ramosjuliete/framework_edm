# Technical Documentation — ResultsAnalysis (with practical examples)

This class performs analyses on **cluster results** already obtained, including descriptive statistics,
significance tests, SRL profile descriptions, and generation of comparative charts.

> **Stack assumed in the examples:** `pandas`, `scipy.stats`, `matplotlib`

## Table of Contents
- [Overview](#overview)
- [Installation & prerequisites](#installation--prerequisites)
- [Recommended workflow](#recommended-workflow)
- [Class API](#class-api)
- [End-to-end usage example](#end-to-end-usage-example)
- [Best practices](#best-practices)

## Overview
Receives a DataFrame with clusters assigned to users and columns of interest. It allows evaluating statistical differences between groups and describing self-regulated learning profiles.

## Installation & prerequisites
```bash
pip install pandas scipy matplotlib
```

## Recommended workflow
1. Generate `df_clusters` after applying clustering methods.
2. Compute descriptive statistics by cluster.
3. Perform significance tests to check differences between groups.
4. Generate SRL tables/profiles and supporting visualizations.

---

## Class API
### `__init__(algorithm, fileCluster, separatorFileCluster)`
**Parameters:** `algorithm, fileCluster, separatorFileCluster`

**Example:**
```python
ra.__init__(algorithm, fileCluster, separatorFileCluster)
```

### `loadFile()`
**Parameters:** `—`

**Example:**
```python
ra.loadFile()
```

### `removeIdentifierColumns(dataframe)`
**Parameters:** `dataframe`

**Example:**
```python
ra.removeIdentifierColumns(df_clusters)
```

### `statisticalByClusters(df)`
**Parameters:** `df`

**Example:**
```python
ra.statisticalByClusters(df_clusters)
```

### `statisticalSignificance(dataframe, significance_level)`
**Parameters:** `dataframe, significance_level`

**Example:**
```python
ra.statisticalSignificance(df_clusters, significance_level)
```

### `checkProfileSRL(dataframe)`
**Parameters:** `dataframe`

**Example:**
```python
ra.checkProfileSRL(df_clusters)
```

### `profileSRLdescription(dataframe, fileGrade, separatorFileGrade)`
**Parameters:** `dataframe, fileGrade, separatorFileGrade`

**Example:**
```python
ra.profileSRLdescription(df_clusters, fileGrade, separatorFileGrade)
```

### `profileSRLGraphics(dataframe, fileGrade, separatorFileGrade, path, show_outliers)`
**Parameters:** `dataframe, fileGrade, separatorFileGrade, path, show_outliers`

**Example:**
```python
ra.profileSRLGraphics(df_clusters, fileGrade, separatorFileGrade, "out/", show_outliers)
```

### `plotGraphicClusters(dataframe, rows, columns, type_graphic, path, show_outliers)`
**Parameters:** `dataframe, rows, columns, type_graphic, path, show_outliers`

**Example:**
```python
ra.plotGraphicClusters(df_clusters, rows, columns, type_graphic, "out/", show_outliers)
```



## End-to-end usage example

```python
import pandas as pd
from resultsanalysis import ResultsAnalysis

# Example of a clustered DataFrame
df_clusters = pd.DataFrame({
    "iduser": [1,2,3,4,5,6,7,8,9,10],
    "cluster": [0,0,1,1,2,2,0,1,2,0],
    "time": [1200, 850, 930, 4000, 2100, 760, 1800, 3000, 2500, 1100],
    "SRL_Planning": [5,3,4,10,6,2,5,8,7,3],
    "SRL_Monitoring": [4,2,3,9,5,1,4,7,6,2],
    "SRL_Evaluation": [2,1,2,6,3,1,2,5,4,1],
    "TotalEvents": [80,55,61,150,98,40,77,130,115,60],
    "grade": [7.5,6.0,8.0,9.5,5.5,6.5,7.0,8.5,9.0,6.0]
})

ra = ResultsAnalysis(path="out/")

# 1) Descriptive statistics by cluster
ra.statisticalByClusters(df_clusters)

# 2) Statistical significance tests between clusters
ra.statisticalSignificance(df_clusters)

# 3) Descriptive SRL profile by cluster
ra.profileSRLdescription(df_clusters)

# 4) SRL profile charts by cluster (saved to disk)
ra.profileSRLGraphics(df_clusters)
```



## Best practices
- Use `df_clusters` with columns: `iduser`, `cluster`, `time`, `SRL_Planning`, `SRL_Monitoring`, `SRL_Evaluation`, `TotalEvents`, `grade`.
- Ensure that `cluster` is an integer and contains no null values.
- Clearly separate input features (SRL/time/events) and output variables (grades/performance).
- Statistical tests assume certain distributions; check normality before choosing parametric or non-parametric tests.
