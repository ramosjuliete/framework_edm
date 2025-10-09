# Technical Documentation — Clustering

The **Clustering** class runs clustering techniques (K-Means, Agglomerative/Hierarchical, HDBSCAN, DBSCAN, Gaussian Mixtures) over educational datasets to detect student groups and behavior patterns.  

- Input: numeric DataFrame  
- Output: cluster labels, quality metrics (silhouette, Dunn/DB), plots  

Main API includes:  
- Model selection helpers: `bestValueK_SilhouetteScores`, `bestValueK_Elbow`, `bestValueK_forAgglomerative`  
- Algorithms: `kmeans`, `agglomerative`, `hdbscan`, `dbscan`, `gaussian`  
- Validation: `dunn_index`, `internalValidation`  
- Saving/export: `saveClustering`  

**Best practices:** standardize features, set `random_state`, check sample sizes, validate clusters with domain experts.  
