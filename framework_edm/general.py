import sys
import io
from framework_edm.exploratoryanalysis import ExploratoryAnalysis
from framework_edm.clustering import Clustering
from framework_edm.resultsanalysis import ResultsAnalysis
class General:
    def __init__(self, fileDataset, delimiterDataset, path):
        self.dataset = fileDataset
        self.delimiterDataset = delimiterDataset
        self.path = path

    def execute(self, algorithm, fileGrade, delimiterGrade, **kwargs):
        # --- Classe ExploratoryAnalysis ---
        ea = ExploratoryAnalysis(self.dataset, self.delimiterDataset)
        df_explory = ea.loadDataframe()
        ea.statisticalDescription(df_explory)
        ea.applyNormalityTest(df_explory, 'smirnov')
        ea.createSpearmanMatrix(df_explory, self.path)

        # --- Classe Clustering ---
        cluster = Clustering(algorithm, self.path)
        fileCluster = ''

        if algorithm == "kmeans":
            k = kwargs.get("k")
            if k is None:
                raise ValueError("O algoritmo kmeans exige o parâmetro 'k'")
            fileCluster = cluster.kmeans(df_explory, k)

        elif algorithm == "agglomerative":
            n_clusters = kwargs.get("n_clusters")
            if n_clusters is None:
                raise ValueError("O algoritmo Agglomerative exige o parâmetro 'n_clusters'")
            fileCluster = cluster.agglomerative(df_explory, n_clusters)

        elif algorithm == "gaussian":
            n_clusters = kwargs.get("n_clusters")
            if n_clusters is None:
                raise ValueError("O algoritmo Agglomerative exige o parâmetro 'n_clusters'")
            fileCluster = cluster.gaussian(df_explory, n_clusters)

        elif algorithm == "hdbscan":
            min_samples = kwargs.get("min_samples")
            min_cluster_size = kwargs.get("min_cluster_size")
            if min_samples is None or min_cluster_size is None:
                raise ValueError("O algoritmo hdbscan exige 'min_samples' e 'min_cluster_size'")
            fileCluster = cluster.hdbscan(df_explory, min_samples, min_cluster_size)
        
        elif algorithm == "dbscan":
            value_eps = kwargs.get("value_eps")
            value_minsamples = kwargs.get("value_minsamples")
            if value_eps is None or value_minsamples is None:
                raise ValueError("O algoritmo dbscan exige 'value_eps' e 'value_minsamples'")
            fileCluster = cluster.dbscan(df_explory, value_eps, value_minsamples)

        else:
            raise ValueError(f"Algoritmo {algorithm} não suportado")

        # --- Classe ResultsAnalysis ---
        ra = ResultsAnalysis(algorithm, fileCluster, ';')
        df_cluster = ra.loadFile()

        # 🔹 Captura os prints em buffer
        buffer = io.StringIO()
        stdout_original = sys.stdout
        sys.stdout = buffer

        try:
            ra.statisticalSignificance(df_cluster, 0.05)
            ra.checkProfileSRL(df_cluster)
            ra.profileSRLdescription(df_cluster, fileGrade, delimiterGrade)
        finally:
            # Restaura o stdout
            sys.stdout = stdout_original

        # 🔹 Salva o conteúdo em arquivo na pasta self.path
        output_file = f"{self.path}{algorithm}_results.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(buffer.getvalue())

        # Gráfico SRL Description e Gráficos de Análises Estatísticas
        ra.profileSRLGraphics(df_cluster, fileGrade, delimiterGrade, self.path, False)

        graficos = ['density', 'boxplot', 'violinplot', 'stripplot']
        for grafico in graficos:
            ra.plotGraphicClusters(df_cluster, 2, 4, grafico, self.path, False)