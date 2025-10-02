
# API Reference — framework_edm
Technical documentation for all public classes and methods in the `framework_edm` package.  
Style: **Google docstring** (rendered here as Markdown).

---

## Table of Contents

- [General](#general)
  - [__init__](#general-__init__)
  - [execute](#general-execute)
- [Clustering](#clustering)
  - [__init__](#clustering-__init__)
  - [kmeans](#clustering-kmeans)
  - [hdbscan](#clustering-hdbscan)
  - [agglomerative](#clustering-agglomerative)
  - [dbscan](#clustering-dbscan)
  - [gaussian](#clustering-gaussian)
  - [silhouetteScore](#clustering-silhouettescore)
  - [calinskiHarabasz](#clustering-calinskiharabasz)
  - [daviesBouldin](#clustering-daviesbouldin)
- [ExploratoryAnalysis](#exploratoryanalysis)
  - [__init__](#exploratoryanalysis-__init__)
  - [describe](#exploratoryanalysis-describe)
  - [normalityTest](#exploratoryanalysis-normalitytest)
  - [correlationMatrix](#exploratoryanalysis-correlationmatrix)
  - [plotDistributions](#exploratoryanalysis-plotdistributions)
- [ResultsAnalysis](#resultsanalysis)
  - [__init__](#resultsanalysis-__init__)
  - [loadFile](#resultsanalysis-loadfile)
  - [removeIdentifierColumns](#resultsanalysis-removeidentifiercolumns)
  - [statisticalByClusters](#resultsanalysis-statisticalbyclusters)
  - [statisticalSignificance](#resultsanalysis-statisticalsignificance)
  - [checkProfileSRL](#resultsanalysis-checkprofilesrl)
  - [profileSRLdescription](#resultsanalysis-profilesrldescription)
  - [profileSRLGraphics](#resultsanalysis-profilesrlgraphics)
  - [profileSRL`](#resultsanalysis-profilesrl)
- [MinimalDataset](#minimaldataset)
  - [__init__](#minimaldataset-__init__)
  - [loadFile](#minimaldataset-loadfile)
  - [createSRLFileByDefaults](#minimaldataset-createsrlfilebydefaults)
  - [generateSRLFileMap](#minimaldataset-generatesrlfilemap)
  - [generateMinimalDataset](#minimaldataset-generateminimaldataset)

> **Note**: Method names reflect the current code base. Some internal details have been inferred for documentation clarity.

---

## General
High-level orchestrator for the full EDM pipeline: exploratory analysis → clustering → post-cluster analysis.

### General.__init__
Initializes the pipeline with dataset and output path.

**Args:**
  - `fileDataset (str)`: Path to the main dataset file (CSV).
  - `delimiterDataset (str)`: Field delimiter used in `fileDataset` (e.g., `","` or `";"`).
  - `path (str)`: Output folder where results (plots, CSVs) will be saved.

**Simple Example:**
```python
from framework_edm import General
g = General("data.csv", ",", "results/")
```

**Practical Example:**
```python
from framework_edm import General
pipeline = General("data/generaldataset_SQL.csv", ";", "results/SQL/")
```

### General.execute
Runs the selected algorithm end-to-end. For K-Means, optionally associates cluster results with a separate student grade file.

**Args:**
  - `algorithm (str)`: Clustering algorithm name. Supported: `"kmeans"`.
  - `fileGrade (str, optional)`: Path to a CSV with student grades (schema: `iduser, firstname, lastname, grade`). Defaults to `None`.
  - `delimiterGrade (str, optional)`: Delimiter used in the grade file. Required if `fileGrade` is provided.
  - `normalityTeste (bool, optional)`: Whether to run normality tests during analysis (if supported downstream).

**Returns:**
  - `None`

**Simple Example (without grades):**
```python
from framework_edm import General
g = General("data/interactions.csv", ",", "results/")
g.execute("kmeans", k=3)
```

**Practical Example (with grades):**
```python
from framework_edm import General
fileDataset = "H:/.../generaldataset_SQL.csv"
delimiter = ";"
output = "H:/.../RESULTS_SQL/"
g = General(fileDataset, delimiter, output)

# The grade file must follow: iduser, firstname, lastname, grade
g.execute("kmeans", fileGrade="H:/.../stundents_grade.csv", delimiterGrade=",", k=2)
```

---

## Clustering
Implements clustering algorithms and validation metrics.

### Clustering.__init__
Creates a clustering helper with the processed dataset.

**Args:**
  - `dataframe (pandas.DataFrame)`: Input features for clustering.

**Simple Example:**
```python
from framework_edm.clustering import Clustering
c = Clustering(df)
```

**Practical Example:**
```python
c = Clustering(features_df)  # features_df already cleaned and scaled
```

### Clustering.runKmeans
Runs K-Means clustering and returns labels/centroids.

**Args:**
  - `k (int)`: Number of clusters.
  - `random_state (int, optional)`: Seed for reproducibility.

**Returns:**
  - `numpy.ndarray`: Cluster labels for each row.
  - `numpy.ndarray`: Centroids (if exposed by implementation).

**Simple Example:**
```python
labels = c.runKmeans(k=3)
```

**Practical Example:**
```python
labels = c.runKmeans(k=2, random_state=42)
```

### Clustering.runHDBSCAN
Runs HDBSCAN clustering (density-based).

**Args:**
  - `min_samples (int)`: Minimum samples for a dense region.
  - `allow_outliers (bool, optional)`: Whether to keep noise as -1 labels.

**Returns:**
  - `numpy.ndarray`: Cluster labels.

**Simple Example:**
```python
labels = c.runHDBSCAN(min_samples=5)
```

**Practical Example:**
```python
labels = c.runHDBSCAN(min_samples=10, allow_outliers=True)
```

### Clustering.runAgglomerative
Runs Agglomerative (hierarchical) clustering.

**Args:**
  - `k (int)`: Number of clusters.
  - `linkage (str, optional)`: Linkage criterion (`"ward"`, `"complete"`, `"average"`...).

**Returns:**
  - `numpy.ndarray`: Cluster labels.

**Simple Example:**
```python
labels = c.runAgglomerative(k=3)
```

**Practical Example:**
```python
labels = c.runAgglomerative(k=4, linkage="ward")
```

### Clustering.silhouetteScore
Computes the Silhouette score for given features and labels.

**Args:**
  - `X (array-like)`: Feature matrix.
  - `labels (array-like)`: Cluster labels.

**Returns:**
  - `float`: Silhouette coefficient.

**Simple Example:**
```python
score = c.silhouetteScore(X, labels)
```

**Practical Example:**
```python
score = c.silhouetteScore(scaled_df.values, labels)
```

### Clustering.calinskiHarabasz
Computes the Calinski–Harabasz index.

**Args:**
  - `X (array-like)`: Feature matrix.
  - `labels (array-like)`: Cluster labels.

**Returns:**
  - `float`: CH score.

**Simple Example:**
```python
ch = c.calinskiHarabasz(X, labels)
```

**Practical Example:**
```python
ch = c.calinskiHarabasz(scaled_df.values, labels)
```

### Clustering.daviesBouldin
Computes the Davies–Bouldin index.

**Args:**
  - `X (array-like)`: Feature matrix.
  - `labels (array-like)`: Cluster labels.

**Returns:**
  - `float`: DB index (lower is better).

**Simple Example:**
```python
db = c.daviesBouldin(X, labels)
```

**Practical Example:**
```python
db = c.daviesBouldin(scaled_df.values, labels)
```

---

## ExploratoryAnalysis
Exploratory statistics and visualization utilities.

### ExploratoryAnalysis.__init__
Initializes with a dataframe, optional columns to ignore, and output path.

**Args:**
  - `dataframe (pandas.DataFrame)`: Input dataset.
  - `ignore_columns (list[str], optional)`: Columns not to analyze.
  - `path (str, optional)`: Output folder for plots/reports.

**Simple Example:**
```python
from framework_edm.exploratoryanalysis import ExploratoryAnalysis
ea = ExploratoryAnalysis(df)
```

**Practical Example:**
```python
ea = ExploratoryAnalysis(df, ignore_columns=["iduser"], path="results/eda/")
```

### ExploratoryAnalysis.describe
Generates descriptive statistics (mean, std, min, max, etc.).

**Args:**
  - `round_ndigits (int, optional)`: Rounding precision.

**Returns:**
  - `pandas.DataFrame`: Summary table.

**Simple Example:**
```python
summary = ea.describe()
```

**Practical Example:**
```python
summary = ea.describe(round_ndigits=3)
```

### ExploratoryAnalysis.normalityTest
Runs normality tests (e.g., Shapiro, D’Agostino) column-wise.

**Args:**
  - `alpha (float, optional)`: Significance level (default `0.05`).

**Returns:**
  - `pandas.DataFrame`: Test statistics and p-values by column.

**Simple Example:**
```python
norm = ea.normalityTest()
```

**Practical Example:**
```python
norm = ea.normalityTest(alpha=0.01)
```

### ExploratoryAnalysis.correlationMatrix
Computes and optionally plots a correlation matrix.

**Args:**
  - `method (str, optional)`: Correlation method (`"pearson"`, `"spearman"`).

**Returns:**
  - `pandas.DataFrame`: Correlation matrix.

**Simple Example:**
```python
corr = ea.correlationMatrix()
```

**Practical Example:**
```python
corr = ea.correlationMatrix(method="spearman")
```

### ExploratoryAnalysis.plotDistributions
Plots univariate distributions for selected columns.

**Args:**
  - `columns (list[str], optional)`: Columns to plot. If `None`, plots all numeric.

**Returns:**
  - `None`

**Simple Example:**
```python
ea.plotDistributions()
```

**Practical Example:**
```python
ea.plotDistributions(columns=["clicks", "time_on_task", "forum_posts"])
```

---

## ResultsAnalysis
Post-clustering statistical analysis and SRL profiling.

### ResultsAnalysis.__init__
Initializes the analyzer with cluster output.

**Args:**
  - `algorithm (str)`: Algorithm name used (e.g., `"kmeans"`).
  - `fileCluster (str)`: Path to the CSV with data + cluster labels.
  - `separatorFileCluster (str)`: Delimiter used in `fileCluster`.

**Simple Example:**
```python
from framework_edm.resultsanalysis import ResultsAnalysis
ra = ResultsAnalysis("kmeans", "results/clustered.csv", ",")
```

**Practical Example:**
```python
ra = ResultsAnalysis("kmeans", "results/sql/clustered_SQL.csv", ";")
```

### ResultsAnalysis.loadFile
Loads the clustered dataset from disk.

**Returns:**
  - `pandas.DataFrame`: Loaded dataframe.

**Simple Example:**
```python
df = ra.loadFile()
```

**Practical Example:**
```python
clustered_df = ra.loadFile()
```

### ResultsAnalysis.removeIdentifierColumns
Drops identifier columns that should not be included in statistics.

**Args:**
  - `dataframe (pandas.DataFrame)`: Input data.

**Returns:**
  - `pandas.DataFrame`: Cleaned dataframe.

**Simple Example:**
```python
clean = ra.removeIdentifierColumns(df)
```

**Practical Example:**
```python
clean = ra.removeIdentifierColumns(clustered_df)
```

### ResultsAnalysis.statisticalByClusters
Computes basic statistics per cluster (mean, count, etc.).

**Args:**
  - `df (pandas.DataFrame)`: Data containing a cluster column.

**Returns:**
  - `pandas.DataFrame`: Aggregated stats by cluster.

**Simple Example:**
```python
stats = ra.statisticalByClusters(clean)
```

**Practical Example:**
```python
stats = ra.statisticalByClusters(clean)
```

### ResultsAnalysis.statisticalSignificance
Runs significance tests across clusters for each feature.

**Args:**
  - `dataframe (pandas.DataFrame)`: Input data.
  - `significance_level (float)`: Alpha threshold (e.g., `0.05`).

**Returns:**
  - `pandas.DataFrame`: Features with test statistics/p-values.

**Simple Example:**
```python
sig = ra.statisticalSignificance(clean, significance_level=0.05)
```

**Practical Example:**
```python
sig = ra.statisticalSignificance(clean, significance_level=0.01)
```

### ResultsAnalysis.checkProfileSRL
Identifies SRL-related behavioral patterns per cluster.

**Args:**
  - `dataframe (pandas.DataFrame)`: Input clustered data.

**Returns:**
  - `pandas.DataFrame` or `dict`: SRL indicators per cluster.

**Simple Example:**
```python
srl = ra.checkProfileSRL(clean)
```

**Practical Example:**
```python
srl = ra.checkProfileSRL(clean)
```

### ResultsAnalysis.profileSRLdescription
Generates textual description of SRL profiles; can optionally align with a student grade file.

**Args:**
  - `dataframe (pandas.DataFrame)`: Clustered data.
  - `fileGrade (str, optional)`: Path to student grade CSV.
  - `separatorFileGrade (str, optional)`: Delimiter for the grade file.

**Returns:**
  - `str` or `pandas.DataFrame`: Profile descriptions or table.

**Simple Example:**
```python
desc = ra.profileSRLdescription(clean)
```

**Practical Example:**
```python
desc = ra.profileSRLdescription(clean, fileGrade="data/grades.csv", separatorFileGrade=",")
```

### ResultsAnalysis.profileSRLGraphics
Creates SRL-related plots, optionally merging with a grade file.

**Args:**
  - `dataframe (pandas.DataFrame)`: Clustered data.
  - `fileGrade (str, optional)`: Path to student grade CSV.
  - `separatorFileGrade (str, optional)`: Delimiter for the grade file.

**Returns:**
  - `None`

**Simple Example:**
```python
ra.profileSRLGraphics(clean)
```

**Practical Example:**
```python
ra.profileSRLGraphics(clean, fileGrade="data/grades.csv", separatorFileGrade=",")
```

### ResultsAnalysis.profileSRL
End-to-end SRL profiling wrapper that orchestrates description, graphics, and (optionally) grade alignment.

**Args:**
  - `dataframe (pandas.DataFrame)`: Clustered data.

**Returns:**
  - `dict` or `pandas.DataFrame`: Consolidated SRL profile artifacts.

**Simple Example:**
```python
profile = ra.profileSRL(clean)
```

**Practical Example:**
```python
profile = ra.profileSRL(clean)
```

---

## MinimalDataset
Tools to transform raw logs (e.g., Moodle) into compact analysis-ready datasets and SRL maps.

### MinimalDataset.__init__
Initializes the transformer with default SRL mapping file and output path.

**Args:**
  - `defaultSRLFile (str)`: Path to a default SRL strategy map (CSV).
  - `delimiterSRL (str)`: Delimiter used in the SRL map file.
  - `path (str)`: Output folder for generated files.

**Simple Example:**
```python
from framework_edm.minimaldataset import MinimalDataset
md = MinimalDataset("config/srl_default.csv", ",", "results/minimal/")
```

**Practical Example:**
```python
md = MinimalDataset("mapping/default_srl.csv", ";", "out/minimal/")
```

### MinimalDataset.loadFile
Loads a CSV file (e.g., raw log) into memory.

**Returns:**
  - `pandas.DataFrame`: Loaded dataframe.

**Simple Example:**
```python
df = md.loadFile("logs/moodle_log.csv", ";")
```

**Practical Example:**
```python
logs = md.loadFile("data/moodle_logs.csv", ",")
```

### MinimalDataset.createSRLFileByDefaults
Creates a standard SRL mapping file from defaults (if a specific map is not provided).

**Args:**
  - `path (str)`: Output path.

**Returns:**
  - `str`: Path to the generated SRL file.

**Simple Example:**
```python
srl_file = md.createSRLFileByDefaults("out/srl/")
```

**Practical Example:**
```python
srl_file = md.createSRLFileByDefaults("results/srl/")
```

### MinimalDataset.generateSRLFileMap
Generates an SRL mapping by joining raw logs with a default SRL map.

**Args:**
  - `path (str)`: Output folder.
  - `fileLog (str)`: Path to raw log file (CSV).
  - `delimiterLog (str)`: Delimiter for the log file.
  - `defaultSRLFile (str)`: Path to the default SRL map.
  - `delimiterSRL (str)`: Delimiter for the SRL map.

**Returns:**
  - `str`: Path to the generated SRL mapping file.

**Simple Example:**
```python
out = md.generateSRLFileMap("out/", "logs/moodle.csv", ",", "mapping/srl.csv", ",")
```

**Practical Example:**
```python
out = md.generateSRLFileMap(
    path="results/",
    fileLog="data/moodle_logs.csv",
    delimiterLog=",",
    defaultSRLFile="mapping/default_srl.csv",
    delimiterSRL=","
)
```

### MinimalDataset.generateMinimalDataset
Builds a minimal dataset (features only) from the joined/processed logs and mappings.

**Args:**
  - `path (str)`: Output folder.
  - `dataframe (pandas.DataFrame)`: Input logs already preprocessed/joined.

**Returns:**
  - `str` or `pandas.DataFrame`: Path to the generated dataset or the dataframe itself.

**Simple Example:**
```python
mini = md.generateMinimalDataset("out/", logs_df)
```

**Practical Example:**
```python
mini = md.generateMinimalDataset("results/datasets/", logs_with_srl_df)
```

---

> This API reference documents the public surface inferred from the source code. Depending on your version, some parameters may differ slightly. Always consult inline docstrings or source for definitive behavior.
