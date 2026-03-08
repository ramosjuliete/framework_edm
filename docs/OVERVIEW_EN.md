# 📖 SRL Analysis Framework — Overview

This document presents the official technical overview of the **SRL Analysis Framework**, developed within the context of this research. The framework supports the complete **Educational Data Mining (EDM) pipeline** for identifying behavioral patterns associated with **Self-Regulated Learning (SRL)** from interaction data collected in Virtual Learning Environments (VLEs). :contentReference[oaicite:0]{index=0}

---

# 🏗 Framework Architecture

The framework follows a **layered architecture** composed of three main layers:

1. **Input Layer**
2. **Processing Layer**
3. **Output Layer**

This modular architecture supports the full **Educational Data Mining workflow**, ensuring **low coupling, high cohesion, and component independence**, allowing the framework to be applied to different educational datasets as long as the required minimal data structure is respected.

### Input Layer

Responsible for **data preprocessing and standardization**, including cleaning, filtering, and transformation operations.  
These operations are implemented through the `MinimalDataset` class.

### Processing Layer

Implements the **core analytical mechanisms** of the framework, including:

- Exploratory data analysis
- Statistical exploration
- Clustering algorithms for behavioral pattern detection

These functionalities are implemented through the classes:

- `ExploratoryAnalysis`
- `Clustering`

### Output Layer

Responsible for **consolidating the analytical results**, including:

- cluster interpretation
- statistical evaluation
- graphical visualization of behavioral patterns

These functionalities are implemented through the `ResultsAnalysis` class.

---

# 🧩 Framework Diagrams

Two main diagrams describe the internal architecture and execution flow of the framework.

---

## Class Diagram

The **Class Diagram** represents the internal structure of the framework, showing the main classes, their attributes, methods, and relationships.  
It provides a conceptual overview of how the system components interact and how the analytical workflow is organized.

![Framework Class Diagram](_DiagramaClasse.png.png)

---

## Sequence Diagram

The **Sequence Diagram** illustrates the execution flow of the **data analysis stage** coordinated by the `General` class.  
This class acts as the orchestrator that integrates exploratory analysis, clustering, and results interpretation based on a previously constructed **minimal dataset**.

![Framework Sequence Diagram](DiagramaDeSequencia_Orquestrador.png.png)

---

# 🚀 Framework Flow

The framework execution follows the sequence below:

1. **MinimalDataset** → preparation of the minimal dataset from raw Moodle platform events  
2. **ExploratoryAnalysis** → exploratory analysis, descriptive statistics, and correlation analysis  
3. **Clustering** → execution of clustering algorithms (KMeans, DBSCAN, HDBSCAN, etc.)  
4. **ResultsAnalysis** → evaluation of clusters and interpretation of SRL behavioral profiles  
5. **General** → orchestrator that integrates the exploratory analysis, clustering, and results analysis stages from a dataset structured in the minimal dataset format

---

# 📚 Detailed Documentation by Class

- [MinimalDataset](MinimalDataset_EN.md)  
- [ExploratoryAnalysis](ExploratoryAnalysis_EN.md)  
- [Clustering](Clustering_EN.md)  
- [ResultsAnalysis](ResultsAnalysis_EN.md)  
- [General](General_EN.md)

---

🔗 See the files above for the **complete technical documentation of each class**, including parameters, methods, and usage examples.