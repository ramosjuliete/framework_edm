#classe para analisar os resultados do agrupamento após resultados obtidos pela classe clustering
import pandas as pd
import numpy as np
from scipy import stats
import os
import matplotlib.pyplot as plt
import seaborn as sns
import scikit_posthocs as sp
from collections import defaultdict
import warnings
warnings.simplefilter("ignore")
class ResultsAnalysis:

    def __init__(self, algorithm,  fileCluster, separatorFileCluster):
        self.algorithm = algorithm
        self.fileCluster = fileCluster
        self.separatorFileCluster = separatorFileCluster    


    def removeIdentifierColumns(self, dataframe):
        # Colunas a remover
        remove_columns = ['iduser','name']
        # Verifica e remove as colunas existentes
        existing_columns = [col for col in remove_columns if col in dataframe.columns]
        if existing_columns:
            dataframe = dataframe.drop(columns=existing_columns)
        return dataframe

        
    def loadFile(self):
        df = pd.read_csv(self.fileCluster, delimiter=self.separatorFileCluster)
        if 'name' in df.columns:
            df = df.drop(columns=['name'])
        return df

    def statisticalByClusters(self, df):
        #print('método que mostra as descrições estatísticas de cada cluster')
        unique_clusters = df['cluster'].unique()
        print(f"Number of Clusters: {len(unique_clusters)}")
        print(f"Clusters labels: {unique_clusters}")

        dfs_by_cluster = {cluster: df[df['cluster'] == cluster].reset_index(drop=True) for cluster in unique_clusters}

        for cluster, df_cluster in dfs_by_cluster.items():
            print(f"\nCluster {cluster} Statistics :")
            print(df_cluster.describe())
    
    def statisticalSignificance(self, dataframe, significance_level):
        #remover os atributos identificadores
        df_cluster = self.removeIdentifierColumns(dataframe)
        #encontrando a quantidade de clusters
        unique_clusters = df_cluster["cluster"].unique()
        valid_clusters = [c for c in unique_clusters if c != -1]

        if len(unique_clusters) == 2:
            print(f'** Two clusters were found; therefore, we will apply the Mann-Whitney U test. **')

            # Automatically assign clusters
            cluster_a, cluster_b = unique_clusters

            df_cluster_a = df_cluster[df_cluster['cluster'] == cluster_a]
            df_cluster_b = df_cluster[df_cluster['cluster'] == cluster_b]

            # Apply the Mann-Whitney U test for each numeric column (excluding 'cluster')
            mannwhitney_results = {}

            for column in df_cluster.columns[:-1]:  # Excluding 'cluster'
                stat, p_value = stats.mannwhitneyu(df_cluster_a[column], df_cluster_b[column])
                mannwhitney_results[column] = {'U statistic': stat, 'p-value': p_value}

            # Display the results
            df_results = pd.DataFrame(mannwhitney_results).T
            print(f'\nStatistical Results:\n{df_results}')

            # Interpretation of Results
            print("\nInterpretation of Results:")
            for column, values in mannwhitney_results.items():
                p_value = values['p-value']
                if p_value < significance_level:
                    print(f" - {column}: ✨ Significant difference between clusters (p-value={p_value:.4f})")
                else:
                    print(f" - {column}: ✅ No significant difference between clusters (p-value={p_value:.4f})")

        elif len(valid_clusters)>2:
            print(f'** More than two clusters were found; therefore, we will apply the Kruskal-Wallis test and the Dunn test. **')

            # Counter to track which cluster appears most frequently in significant differences
            difference_counter = defaultdict(int)

            # Filter valid clusters (removing -1 if present)
            valid_clusters = [cluster for cluster in df_cluster["cluster"].unique() if cluster != -1]

            # Loop through numerical features to apply statistical tests
            for feature in df_cluster.columns[:-1]:  # Excluding the 'cluster' column
                print(f"\n🔹 Testing attribute: {feature}")

                # Separating values by cluster (only valid clusters)
                groups = [df_cluster[df_cluster["cluster"] == cluster][feature] for cluster in valid_clusters]

                # Step 1: Kruskal-Wallis Test
                stat, p = stats.kruskal(*groups)
                print(f"   - H Statistic = {stat:.4f}, p-value = {p:.4f}")

                # If a significant difference is found (p < 0.05), apply Dunn's test
                if p < significance_level:
                    print("   ✨ Statistically significant difference found! Applying Dunn's test...")

                    # 📌 Step 2: Dunn's Test for multiple comparisons (only valid clusters)
                    df_filtered = df_cluster[df_cluster["cluster"].isin(valid_clusters)]
                    dunn_results = sp.posthoc_dunn(df_filtered, val_col=feature, group_col='cluster', p_adjust='bonferroni')

                    print("   🔍 Dunn's Test Results (adjusted p-values):")
                    print(dunn_results)

                    # 🔹 Counting how often each cluster appears in significant differences
                    for i, row in enumerate(dunn_results.index):
                        for j, col in enumerate(dunn_results.columns):
                            if i < j:  # Avoid duplicate comparisons
                                p_dunn = dunn_results.loc[row, col]
                                if p_dunn < significance_level:
                                    print(f"    Cluster {row} is significantly different from Cluster {col} (p = {p_dunn:.4f})")
                                    difference_counter[row] += 1
                                    difference_counter[col] += 1
                else:
                    print("   ✅ No significant differences between clusters for this feature.")

            # 🔹 Displaying the clusters most frequently found as different
            print("\n📊 **Summary: Clusters that appeared most frequently as different**")
            sorted_clusters = sorted(difference_counter.items(), key=lambda x: x[1], reverse=True)
            for cluster, count in sorted_clusters:
                print(f"   - Cluster {cluster}: {count} occurrences of significant difference")
        else: 
            print("❌ Error: At least two clusters are required to perform a statistical significance test.")

    def plotGraphicClusters(self, dataframe, rows, columns,type_graphic, path):
        print('método para criar e salvar os boxplot de comparação dos dois clusters')
        numeric_columns = dataframe.columns[1:-1]

        # Criar novo DataFrame sem colunas desnecessárias
        df_cluster = dataframe.drop(columns=['iduser'])

        # Garantir que apenas as colunas numéricas sejam usadas, excluindo 'cluster'
        list_columns = [col for col in df_cluster.columns if col != 'cluster']

        # Configurar a grade do gráfico
        plt.figure(figsize=(16, 8))  # Ajustando o tamanho da figura
        num_subplots = len(list_columns)  # Definir o número correto de subgráficos

        # Criar os boxplots
        for i, col in enumerate(list_columns, 1):  # Agora, 'cluster' não será incluído
            plt.subplot(rows, columns, i)
            if(type_graphic=='boxplot'):
                sns.boxplot(x='cluster', y=col, data=df_cluster, hue='cluster', palette="Set2", legend=False)
            elif(type_graphic=='violinplot'):
                sns.violinplot(x='cluster', y=col, data=df_cluster, hue='cluster', palette="Set2", legend=False)
            elif(type_graphic=='stripplot'):
                sns.stripplot(x='cluster', y=col, data=df_cluster, hue='cluster', palette="Set2", legend=False)
            elif(type_graphic=='density'):
                sns.kdeplot(data=df_cluster, x=col,hue='cluster',fill=True, common_norm=False, palette="Set2")
            else:
                print('Unsupported chart type!\nChoose: boxplot, violinplot, stripplot or density to generate the plot')
            plt.title(col)  # Adiciona título para melhor visualização

        plt.tight_layout()
        plt.savefig(path+self.algorithm+type_graphic+'.png')
        print(f'{type_graphic} for {self.algorithm} algorithm saved in {path}')
        plt.show()
    
    def checkProfileSRL(self, df):
        # Seleciona as colunas numéricas, excluindo a coluna 'cluster'
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        numeric_cols.remove('cluster')
        numeric_cols.remove('iduser')
        # Dicionário para armazenar os resultados
        results = {}

        # Para cada coluna, compara as estatísticas e aplica o teste de Mann-Whitney U
        for col in numeric_cols:
            group0 = df[df['cluster'] == 0][col]
            group1 = df[df['cluster'] == 1][col]
    
            # Calcular média e mediana para cada grupo
            mean0, median0 = group0.mean(), group0.median()
            mean1, median1 = group1.mean(), group1.median()

            # Aplica o teste de Mann-Whitney U
            stat, p_value = stats.mannwhitneyu(group0, group1)
    
            # Define qual cluster apresenta valor maior (utilizando média)
            if p_value < 0.05:
                if mean0 > mean1:
                    maior = "Cluster 0"
                elif mean1 > mean0:
                    maior = "Cluster 1"
                else:
                    maior = "Both (equal)"
                result_text = (f"{maior} has a higher average.")
            else:
                result_text = f"No statistically significant difference (p={p_value:.4f})."
    
            results[col] = {
                'mean_cluster_0': mean0,
                'median_cluster_0': median0,
                'mean_cluster_1': mean1,
                'median_cluster_1': median1,
                'p_value': p_value,
                'result': result_text
            }

        # Converter os resultados para um DataFrame para visualização
        results_df = pd.DataFrame(results).T
        print("\nFeatures Details:")
        print(results_df, "\n")

        # Contagem para determinar qual cluster possui maiores médias na maioria das features 
        # (considera apenas features com diferença estatisticamente significativa)
        count_cluster0 = 0
        count_cluster1 = 0
        for col, res in results.items():
            if res['p_value'] < 0.05:
                if res['mean_cluster_0'] > res['mean_cluster_1']:
                    count_cluster0 += 1
                elif res['mean_cluster_1'] > res['mean_cluster_0']:
                    count_cluster1 += 1

        # Exibir resultado global
        print("Result Analysis:")
        if count_cluster0 > count_cluster1:
            print(f"Cluster 0 presents higher averages in {count_cluster0} of the features (significant difference). We consider Cluster 0 with SRL Profile!\n")
        elif count_cluster1 > count_cluster0:
            print(f"Cluster 1 presents higher averages in {count_cluster1} of the features (significant difference). We consider Cluster 1 with SRL Profile!\n")
        else:
            print("Both clusters have similar performance in the averages of the analyzed features. No SRL profile considered!\n")
        

    def profileSRLdescription(self, dataframe, fileGrade, separatorFileGrade):
        #chamando métodos de checagem de perfil SRL dentre os dois clusters considerando media e mediana maior com diferença estatística
        self.checkProfileSRL(dataframe)
        #leitura do arquivo de notas
        dfGrade = pd.read_csv(fileGrade, delimiter=separatorFileGrade)
        #Caso a coluna grade seja do tipo object, ou seja, formato "9,6", converte-se para padrão 9.6
        if dfGrade["grade"].dtype == object:
            dfGrade["grade"] = dfGrade["grade"].str.replace(",", ".", regex=False)

        #depois verifica-se se a coluna grade não é numérica, fazemos a parte, pois pode ter casos de "9.5"
        #caso não seja numérico, realiza-se a conversão
        if not pd.api.types.is_numeric_dtype(dfGrade["grade"]):
            # Converter a coluna "grade" para numérico (float)
            dfGrade["grade"] = pd.to_numeric(dfGrade["grade"], errors='coerce')

        # Aplicar a lógica para criar a coluna "status": notas abaixo de 6 representa status C - reprovado
        # notas entre 6 e 8 representam alunos aprovados
        # notas acima de 8 representam alunos também aprovados e com bom rendimento 
        # essa regra pode mudar a cada análise
        dfGrade["status"] = dfGrade["grade"].apply(lambda x: "C" if x < 6 else ("B" if x < 8 else "A"))

        # Fazendo o merge do dataframe de cluster com o dataframe de notas para iniciar a análise de notas por cluster
        df2 = dataframe.merge(dfGrade[['iduser', 'status']], on='iduser', how='left')
        df2 = df2.fillna('C')  # Substituir NaN por 0
        
        # Contar a frequência de cada conceito em cada cluster
        concept_counts = df2.groupby(['cluster', 'status']).size().unstack(fill_value=0)
               
        # Calcula o total e as porcentagens de conceitos em cada clusters
        concept_counts['Total'] = concept_counts[['A','B','C']].sum(axis=1)
        concept_counts['A_pct'] = concept_counts['A'] / concept_counts['Total'] * 100
        concept_counts['B_pct'] = concept_counts['B'] / concept_counts['Total'] * 100
        concept_counts['C_pct'] = concept_counts['C'] / concept_counts['Total'] * 100

        # Exibindo o resultado
        for cluster, row in concept_counts.iterrows():
            a_count = row['A']
            a_pct   = row['A_pct']
            b_count = row['B']
            b_pct   = row['B_pct']
            c_count = row['C']
            c_pct   = row['C_pct']
            print(f"Percentage of Students in the Cluster {cluster}:")
            print(f"   Students with A Status = {a_count} ({a_pct:.2f}%)")
            print(f"   Students with B Status = {b_count} ({b_pct:.2f}%)")
            print(f"   Students with C Status = {c_count} ({c_pct:.2f}%)")
            print("-"*40)

        
    def profileSRLGraphics(self, dataframe, fileGrade, separatorFileGrade, path):
        dfGrade = pd.read_csv(fileGrade, delimiter=separatorFileGrade)
        #Caso a coluna grade seja do tipo object, ou seja, formato "9,6", converte-se para padrão 9.6
        if dfGrade["grade"].dtype == object:
            dfGrade["grade"] = dfGrade["grade"].str.replace(",", ".", regex=False)

        #depois verifica-se se a coluna grade não é numérica, fazemos a parte, pois pode ter casos de "9.5"
        #caso não seja numérico, realiza-se a conversão
        if not pd.api.types.is_numeric_dtype(dfGrade["grade"]):
            # Converter a coluna "grade" para numérico (float)
            dfGrade["grade"] = pd.to_numeric(dfGrade["grade"], errors='coerce')

        # Aplicar a lógica para criar a coluna "status": notas abaixo de 6 representa status C - reprovado
        # notas entre 6 e 8 representam alunos aprovados
        # notas acima de 8 representam alunos também aprovados e com bom rendimento 
        # essa regra pode mudar a cada análise
        dfGrade["status"] = dfGrade["grade"].apply(lambda x: "C" if x < 6 else ("B" if x < 8 else "A"))

        # Fazendo o merge do dataframe de cluster com o dataframe de notas para iniciar a análise de notas por cluster
        df2 = dataframe.merge(dfGrade[['iduser', 'status']], on='iduser', how='left')
        df2 = df2.fillna('C')  # Substituir NaN por 0
        
        # Contar a frequência de cada conceito em cada cluster
        concept_counts = df2.groupby(['cluster', 'status']).size().unstack(fill_value=0)

        # Convert frequencies to percentages
        concept_percentages = concept_counts.div(concept_counts.sum(axis=1), axis=0) * 100

        # Define custom colors for each concept
        colors = ['#1f77b4', '#aec7e8', '#ffbb78']  # Dark blue, light blue, light orange

        # Create a stacked horizontal bar chart with custom colors
        concept_percentages.plot(kind='barh', stacked=True, figsize=(10, 6), color=colors)

        plt.title('Percentage of Students by Grade in Each Cluster')
        plt.xlabel('Percentage (%)')
        plt.ylabel('Cluster')
        plt.yticks(rotation=0)
        plt.legend(title='Grade')
        plt.grid(axis='x', linestyle='--', alpha=0.7)

        # Display the chart
        plt.savefig(path+self.algorithm+'_profileSRL.png')
        print(f'Profile SRL Graphic for {self.algorithm} algorithm saved in {path}')
        plt.show()
    
    