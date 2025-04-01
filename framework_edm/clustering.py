#Classe onde serão aplicados os algoritmos e realizadas as medidas de validação interna, diferenças estatísticas
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from scipy.spatial.distance import cdist
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics.pairwise import euclidean_distances
import hdbscan
from sklearn.cluster import DBSCAN
from sklearn.mixture import GaussianMixture
from kneed import KneeLocator  # Biblioteca para detectar o ponto de inflexão
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from hdbscan import validity_index
import seaborn as sns
import warnings
warnings.simplefilter("ignore")

#Classe para aplicação de diferentes algoritmos de clustering e métodos de escolha de parâmetros
class Clustering:

    def __init__(self, algorithm, path):
        self.algorithm = algorithm
        self.path = path

    def removeIdentifierColumns(self, dataframe):
        # Colunas a remover
        remove_columns = ['iduser','name']
        # Verifica e remove as colunas existentes
        existing_columns = [col for col in remove_columns if col in dataframe.columns]
        if existing_columns:
            dataframe = dataframe.drop(columns=existing_columns)
        return dataframe

    def dendogram_hdbscan(self, dataframe):
        df = self.removeIdentifierColumns(dataframe)
        clusterer = hdbscan.HDBSCAN(min_samples=10, min_cluster_size=20)
        clusterer.fit(df)

        # Plotar o dendrograma de condensação
        plt.figure(figsize=(10, 6))
        clusterer.condensed_tree_.plot(select_clusters=True, selection_palette=sns.color_palette())
        plt.title("Condensation Dendrogram - HDBSCAN")
        plt.savefig(self.path+'condensation_dendrogram_hdbscan.png')
        print(f'Condensation Dendrogram - HDBSCAN saved in {self.path}')
        plt.show()
            
    def analysisMeasuresHDBSCAN(self, dataframe, min_samples_values, min_cluster_size_values):
        #método recebe o dataframe e duas listas com valores de min-samples e min-cluster-sizes
        df = self.removeIdentifierColumns(dataframe)
        best_score = -np.inf
        best_params = None

        print("----Validation measures for the HDBSCAn algorithm\n----")
        for min_samples in min_samples_values:
            for min_cluster_size in min_cluster_size_values:
                clusterer = hdbscan.HDBSCAN(min_samples=min_samples, min_cluster_size=min_cluster_size)
                labels = clusterer.fit_predict(df.values)
        
                # Verificar se há mais de um cluster
                if len(set(labels)) > 1:
                    silhouette = silhouette_score(df.values, labels)
                    db_index = davies_bouldin_score(df.values, labels)
                    validity = validity_index(df.values, labels)
            
                    print(f"min_samples={min_samples}, min_cluster_size={min_cluster_size}, Silhouette={silhouette:.4f}, DB Index={db_index:.4f}, Validity={validity:.4f}")
            
                    # Escolher melhor configuração baseada no validity_score_
                if validity > best_score:
                    best_score = validity
                    best_params = (min_samples, min_cluster_size)

        # Exibir os melhores parâmetros
        print('\n-------------------------------------------------------------------------------------------')
        print(f"Best parameters found considering the Validity Score={best_score:.4f} is: min_samples={best_params[0]}, min_cluster_size={best_params[1]}")
        print(f'The Validity Score is the specific HDBSCAN metric for evaluating the stability of clusters')
        #retorna uma tupla onde o primeiro valor é o min_samples e o segundo é o min_cluster_size
        return best_params

    def bestValueK_SilhouetteScores(self,dataframe):
        df = self.removeIdentifierColumns(dataframe)
        k_values = range(2, 11)
        silhouette_scores = []

        # Calcular o Silhouette Score para cada K
        for k in k_values:
            kmeans = KMeans(n_clusters=k, init='k-means++', random_state=42)
            labels = kmeans.fit_predict(df)
            score = silhouette_score(df, labels)
            silhouette_scores.append(score)

        # Plot do gráfico de Silhouette Score
        plt.figure(figsize=(8, 6))
        plt.plot(k_values, silhouette_scores, marker='o', linestyle='-')
        plt.xlabel('umber of Clusters (K)')
        plt.ylabel('Silhouette Score')
        plt.title('Silhouette Score for different K values')
        plt.grid(True)
        plt.savefig(self.path+'silhouette_scores_analysis.png')
        print(f'Silhouette Scores Graphic saved in {self.path}')
        plt.show()
        # Encontrar o melhor valor de K com base no Silhouette Score
        best_k = k_values[np.argmax(silhouette_scores)]
        print("The best K value for K-Means, based on the Silhouette Score, is:", best_k)
        return best_k
    
    def bestValueK_Elbow(self, dataframe):
        df = self.removeIdentifierColumns(dataframe)
        # Define o intervalo de valores para K
        k_values = range(1, 11)
        inertia_values = []

        # Calcula a inércia (SSE) para cada valor de K
        for k in k_values:
            kmeans = KMeans(n_clusters=k, init='k-means++', random_state=42)
            kmeans.fit(dataframe)
            inertia_values.append(kmeans.inertia_)

        # Utiliza o KneeLocator para detectar o "cotovelo" no gráfico
        knee_locator = KneeLocator(k_values, inertia_values, curve='convex', direction='decreasing')
        best_k = knee_locator.knee

        # Plot do Método do Cotovelo
        plt.figure(figsize=(8, 6))
        plt.plot(k_values, inertia_values, marker='o', linestyle='-', label='Inércia (SSE)')
        plt.xlabel('Number of Clusters (K)')
        plt.ylabel('Intertia (SSE)')
        plt.title('Elbow Method for determining the best value K for K-Means')
        plt.grid(True)

            # Destaca o melhor valor de K no gráfico, se detectado
        if best_k is not None:
            plt.axvline(best_k, linestyle='--', color='r', label=f'Best K-Value: {best_k}')
            plt.legend()

        
        plt.savefig(self.path+'elbow_method.png')
        print(f'Elbow Method figure saved in {self.path}')
        plt.show()
        print("The best K value for K-Means, based on the Elbow Method, is:", best_k)
        return best_k

    def bestValueK_forAgglomerative(self, dataframe):
        df = self.removeIdentifierColumns(dataframe)
        # Criar o linkage para o dendrograma
        linked = linkage(df, method='ward')

        # Avaliação com Silhouette Score para diferentes números de clusters
        k_values = range(2, 11)
        silhouette_scores = []

        for k in k_values:
            agglo = AgglomerativeClustering(n_clusters=k)
            labels = agglo.fit_predict(df)
            score = silhouette_score(df, labels)
            silhouette_scores.append(score)

        # Encontrar o melhor K com base no Silhouette Score
        best_k = k_values[np.argmax(silhouette_scores)]

        # Plot do Dendrograma com linha de corte destacando o melhor K
        plt.figure(figsize=(10, 7))
        dendrogram(linked, truncate_mode='level', p=5)
        plt.axhline(y=linked[-best_k, 2], color='r', linestyle='--', label=f'Cut to K={best_k}')
        plt.title("Dendrogram with Cut Point (Agglomerative Clustering)")
        plt.xlabel("Samples")
        plt.ylabel("Distance")
        plt.legend()
        plt.savefig(self.path+'dendogram_aglomerative_clustering.png')
        print(f'Dendogram Graphic saved in {self.path}')
        plt.show()

        # Plot do Silhouette Score
        plt.figure(figsize=(8, 6))
        plt.plot(k_values, silhouette_scores, marker='o', linestyle='-', color='b', label="Silhouette Score")
        plt.axvline(best_k, linestyle='--', color='r', label=f'Melhor K = {best_k}')
        plt.xlabel('Number de Clusters (K)')
        plt.ylabel('Silhouette Scores')
        plt.title('Silhouette Scores for different numbers of clusters (AgglomerativeClustering)')
        plt.grid(True)
        plt.legend()
        plt.savefig(self.path+'silhouettescores_aglomerative_clustering.png')
        print(f'Silhouette Scores Graphic for Agglomerative Clustering saved in {self.path}')
        plt.show()

        print("The best K value for Agglomerative Clustering, based on the Silhouette Score, is:", best_k)
        return best_k

    def dunn_index(self, X, labels):
        unique_clusters = np.unique(labels)
        if len(unique_clusters) < 2:
            return 0

        # Distâncias inter-cluster: mínima distância entre pontos de clusters diferentes
        inter_dists = []
        for i in unique_clusters:
            for j in unique_clusters:
                if i < j:
                    cluster_i = X[labels == i]
                    cluster_j = X[labels == j]
                    distances = cdist(cluster_i, cluster_j, metric='euclidean')
                    inter_dists.append(np.min(distances))
        min_inter = np.min(inter_dists)

        # Distâncias intra-cluster: máxima distância dentro de cada cluster
        intra_dists = []
        for i in unique_clusters:
            cluster_i = X[labels == i]
            if len(cluster_i) > 1:
                distances = cdist(cluster_i, cluster_i, metric='euclidean')
                # Usamos a distância máxima (excluindo os zeros da diagonal)
                intra_dists.append(np.max(distances))
        max_intra = np.max(intra_dists)
        return min_inter / max_intra

    def internalValidation(self, labels, dataframe):
        silh = silhouette_score(dataframe, labels)
        calin = calinski_harabasz_score(dataframe, labels)
        db_score = davies_bouldin_score(dataframe, labels)
        dunn = self.dunn_index(dataframe, labels)
        print(f'\n Silhuotte: {silh}\n Calinski: {calin}\n Davies-Bouldin: {db_score}\n Dunn-Index: {dunn}')

    def saveClustering(self,dataframe,name):
        dataframe.to_csv(self.path+name+'.csv', sep=';', encoding='utf-8', index=False)
        print(f"\n File Clustering saved in {self.path}")

        #mostrando as primeiras linhas do dataframe salvo --> apagar essa linha depois
        print('\n--------------------Dataframe após clustering!--------------------')
        print(dataframe.head())

    def kmeans(self, dataframe, valueK):
        df = self.removeIdentifierColumns(dataframe)

        #aplicando o algoritmo k-means
        cluster = KMeans(n_clusters=valueK,init='k-means++', random_state=42)
        preds = cluster.fit_predict(df)
        
        #calculando e mostrando as medidas de validação interna
        print(f'Internal Validation Measures for {self.algorithm} Algorithm with K={valueK}')
        self.internalValidation(preds,df)
        print(f' Inertia: {cluster.inertia_}')
        #adicionando coluna cluster no dataframe
        df['cluster'] = cluster.labels_
        
        #salvando o arquivo do k-means para posterior analise dos resultados
        dataframe['cluster'] = df['cluster']
        name = self.algorithm+'_'+str(valueK)
        self.saveClustering(dataframe,name)
        
    def agglomerative(self, dataframe,  numberClusters):
        df = self.removeIdentifierColumns(dataframe)

        cluster = AgglomerativeClustering(n_clusters=numberClusters)
        preds = cluster.fit_predict(df)
        
        #calculando e mostrando as medidas de validação interna
        print(f'Internal Validation Measures for {self.algorithm} Algorithm with Clusters={numberClusters}')
        self.internalValidation(preds,df)
        
        #adicionando coluna cluster no dataframe
        df['cluster'] = cluster.labels_
        
        #salvando o arquivo do k-means para posterior analise dos resultados
        dataframe['cluster'] = df['cluster']
        name = self.algorithm+'_'+str(numberClusters)
        self.saveClustering(dataframe,name)
        
    def hdbscan(self, dataframe, value_min_samples, value_min_cluster_size):
        df = self.removeIdentifierColumns(dataframe)

        hdbscan_model = hdbscan.HDBSCAN(min_samples=value_min_samples, min_cluster_size=value_min_cluster_size, metric='euclidean', gen_min_span_tree=True, p=None)
        preds = hdbscan_model.fit_predict(df)
        
        # Verificar a quantidade de clusters gerados (excluindo ruído, label -1)
        filtered_labels = preds[preds != -1]
        unique_labels = np.unique(filtered_labels)
        num_clusters = len(unique_labels[unique_labels != -1])
        
        #calculando e mostrando as medidas de validação interna
        print(f'Internal Validation Measures for {self.algorithm} Algorithm with {num_clusters} generated clusters')
        validity = validity_index(df.values, preds)
        self.internalValidation(preds,df)
        print(f'Validity Index: {validity}')
        
        #adicionando coluna cluster no dataframe
        df['cluster'] = hdbscan_model.labels_
        
        #salvando o arquivo do k-means para posterior analise dos resultados
        dataframe['cluster'] = df['cluster']
        name = self.algorithm+'_'+str(num_clusters)
        self.saveClustering(dataframe,name)
        

    def dbscan(self, dataframe, value_eps, value_minsamples):
        df = self.removeIdentifierColumns(dataframe)

        dbscan = DBSCAN(eps=value_eps, min_samples=value_minsamples)
        preds = dbscan.fit_predict(df)
        # Verificar a quantidade de clusters gerados (excluindo ruído, label -1)
        n_clusters = len(set(preds)) - (1 if -1 in preds else 0)
        n_noise = list(preds).count(-1)

        print(f'Estimated number of clusters: {n_clusters}')
        print(f'Estimated number of noise points: {n_noise}')
        
        #calculando e mostrando as medidas de validação interna
        print(f'Internal Validation Measures for {self.algorithm} Algorithm with {n_clusters} generated clusters')
        self.internalValidation(preds,df)
        
        #adicionando coluna cluster no dataframe
        df['cluster'] = dbscan.labels_
        
        #salvando o arquivo do k-means para posterior analise dos resultados
        dataframe['cluster'] = df['cluster']
        name = self.algorithm+'_'+str(n_clusters)
        self.saveClustering(dataframe,name)
        
    
    def gaussian(self, dataframe,n_clusters):
        df = self.removeIdentifierColumns(dataframe)

        gmm = GaussianMixture(n_components=n_clusters, random_state=None)
        gmm.fit(df.values)

        preds = gmm.predict(df.values)

        #calculando e mostrando as medidas de validação interna
        print(f'Internal Validation Measures for {self.algorithm} Algorithm with {n_clusters} generated clusters')
        self.internalValidation(preds,df)
        
        #adicionando coluna cluster no dataframe
        df['cluster'] = preds
        
        #salvando o arquivo do k-means para posterior analise dos resultados
        dataframe['cluster'] = df['cluster']
        name = self.algorithm+'_'+str(n_clusters)
        self.saveClustering(dataframe,name)
        