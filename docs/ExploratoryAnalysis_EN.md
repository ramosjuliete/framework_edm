# Technical Documentation — ExploratoryAnalysis

The **ExploratoryAnalysis** class performs statistical exploratory analysis on DataFrames, including descriptive stats, normality tests, correlations, and plots.  

- Input: minimal dataset or equivalent CSV  
- Output: descriptive statistics, normality tests (Shapiro, K-S, Anderson), correlation matrices (Pearson/Spearman), plots  

Main API includes:  
- `statisticalDescription(...)`  
- `createSpearmanMatrix(...)`  
- `shapiro_wilk_test(...)`, `kolmogorov_smirnov_test(...)`, `anderson_darling_test(...)`  
- `applyNormalityTest(...)`  

**Best practices:** consistent column names, handle missing values, choose correlation test based on normality, save plots in a reproducible directory.  
