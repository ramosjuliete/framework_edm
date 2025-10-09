# Technical Documentation — General

The **General** class works as an **orchestrator**: it receives a processed minimal dataset and executes exploratory analysis, clustering, and results analysis in sequence.  

- Input: `minimaldataset.csv`  
- Output: descriptive stats, clusters, results analysis, plots, summary file  

Main API:  
- `__init__(fileDataset, delimiterDataset, path)`  
- `execute(algorithm, fileGrade, delimiterGrade, normalityTeste, ...)`  

**Best practices:** validate dataset format, check delimiter, keep results in separate directories, include expected columns (`iduser`, `time`, SRL features, `TotalEvents`).  
