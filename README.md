# framework_edm

`framework_edm` is a modular pipeline designed for **Exploratory Data Analysis**, **Unsupervised Clustering**, and **Post-Cluster Statistical Profiling**, with a focus on **Educational Data Mining (EDM)** and **Self-Regulated Learning (SRL) behavior analysis**.

It allows users to run a **full end-to-end analysis workflow with a single command**, making it ideal for research workflows or repeatable analytical pipelines.

---

## 📁 Project Structure

```
framework_edm/
│── clustering.py          # Implements multiple clustering algorithms (KMeans, HDBSCAN, Agglomerative, etc.)
│── exploratoryanalysis.py # Statistical summaries, distribution tests, and visualization utilities
│── resultsanalysis.py     # Post-clustering evaluation and SRL-based profiling
│── minimaldataset.py      # Generation of reduced datasets from raw Moodle logs and mapping them to SRL strategies 
│── general.py             # Main pipeline orchestrator (single entry point)
│── __init__.py
```

---

## ⚙️ Installation

You can install the package locally using:

```bash
pip install .
```

Alternatively, for editable development mode:

```bash
pip install -e .
```

Make sure to install the required dependencies before running:

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage Examples

### ✅ Example 1 — Using K-Means WITH student grade file

```python
from framework_edm import General

fileDataset = 'path/to/dataset.csv'
delimiter = ';'
output_folder = 'path/to/RESULTS/'

pipeline = General(fileDataset, delimiter, output_folder)

# The grade file *must* follow the schema: iduser, firstname, lastname, grade
pipeline.execute(
    'kmeans',
    fileGrade='path/to/stundents_grade.csv',
    delimiterGrade=",",
    k=2
)
```

---

### ✅ Example 2 — Using K-Means WITHOUT student grade file

```python
from framework_edm import General

fileDataset = 'path/to/dataset.csv'
delimiter = ';'
output_folder = 'path/to/RESULTS/'

pipeline = General(fileDataset, delimiter, output_folder)

# No grade file provided — clustering runs only on dataset features
pipeline.execute(
    'kmeans',
    k=2
)
```

---

## 📊 Outputs

Depending on configuration, the pipeline may produce:

| Output Type | Description |
|-------------|-------------|
| 📈 Plots / Graphs | Distributions, correlations, or 2D cluster visualizations |
| 📁 CSV Files | Datasets with cluster labels assigned |
| 📄 Statistical Reports | Group comparison tables and validation metrics |
| 🧠 SRL Behavioral Profiles | Interpretation of clusters based on learning behavior |

---

## ✅ Recommended Workflow

1. **Prepare your dataset** in `.csv` or tabular format  
2. **Choose whether to include a student grade file or not**  
3. **Call `General(...).execute('kmeans', k=...)` accordingly**  
4. **Inspect results** in generated outputs (CSV, plots, or printed reports)

---

## 📌 Future Improvements (Optional Roadmap)

- [ ] Auto-generated PDF report summarization
- [ ] Streamlit-based dashboard for interactive exploration
- [ ] Support for temporal / sequential behavioral data

---

## 📄 License

> MIT License — Free for academic and commercial use with attribution.

---

## ✨ Credits

Developed as part of the **framework_edm** initiative for scalable Educational Data Mining workflows.

If you use this framework in research, please acknowledge it where appropriate.
