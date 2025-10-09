# Technical Documentation — ResultsAnalysis

The **ResultsAnalysis** class evaluates **cluster results**, including descriptive statistics, significance tests, SRL profile descriptions, and comparative plots.  

- Input: DataFrame with cluster assignments  
- Output: summary tables, statistical tests, SRL profile tables, visualizations  

Main API includes:  
- `statisticalByClusters(...)`  
- `statisticalSignificance(...)`  
- `checkProfileSRL(...)`  
- `profileSRLdescription(...)`  
- `profileSRLGraphics(...)`  
- `plotGraphicClusters(...)`  

**Best practices:** ensure `cluster` is integer and not null, separate input features from output variables (e.g. grade), check normality before choosing parametric/non-parametric tests.  
