#classe para analisar os resultados do agrupamento após resultados obtidos pela classe clustering
import pandas as pd
import numpy as np
from scipy import stats
import os
import matplotlib.pyplot as plt
import seaborn as sns
import scikit_posthocs as sp
from collections import defaultdict
from scipy.stats import mannwhitneyu, kruskal
import warnings
warnings.simplefilter("ignore")

class ResultsAnalysis:

    def __init__(self, algorithm,  fileCluster, separatorFileCluster):
        self.algorithm = algorithm
        self.fileCluster = fileCluster
        self.separatorFileCluster = separatorFileCluster    
    
    #MÉTODO_1 -> Carrega o datframe a partir do arquivo de cluster (.csv) enviado por parâmetro
    def loadFile(self):
        df = pd.read_csv(self.fileCluster, delimiter=self.separatorFileCluster)
        #caso o atributo name esteja presente, este é removido antes do retorno
        if 'name' in df.columns:
            df = df.drop(columns=['name'])
        return df
    
    #MÉTODO_2 -> Remove atributos identificadores se houver para facilitar comparações em testes estatísticos
    def removeIdentifierColumns(self, dataframe):
        # Colunas a remover
        remove_columns = ['iduser','name']
        # Verifica e remove as colunas existentes
        existing_columns = [col for col in remove_columns if col in dataframe.columns]
        if existing_columns:
            dataframe = dataframe.drop(columns=existing_columns)
        return dataframe

    #MÉTODO_3 -> Mostra a estatística por cluster ao enviar o dataframe que possui a coluna "cluster"
    def statisticalByClusters(self, df):
        #print('método que mostra as descrições estatísticas de cada cluster')
        unique_clusters = df['cluster'].unique()
        print(f"Number of Clusters: {len(unique_clusters)}")
        print(f"Clusters labels: {unique_clusters}")

        dfs_by_cluster = {cluster: df[df['cluster'] == cluster].reset_index(drop=True) for cluster in unique_clusters}

        for cluster, df_cluster in dfs_by_cluster.items():
            print(f"\nCluster {cluster} Statistics :")
            print(df_cluster.describe())
    

    #MÉTODO_4 -> Realiza testes de significância estatística para verificar se há diferenças significativas entre os clusters
    #Dois testes podem ser usados: U de Mann Whitney ou Kruskal Wallis
    def statisticalSignificance(self, dataframe, significance_level):
        #remover os atributos identificadores
        df_cluster = self.removeIdentifierColumns(dataframe)
        #encontrando a quantidade de clusters
        unique_clusters = df_cluster["cluster"].unique()
        valid_clusters = [c for c in unique_clusters if c != -1]

        #teste U de Mann Whitney aplicado quando o número de clusters for 2
        if len(valid_clusters) == 2:
            print(f'** Two clusters were found; therefore, we will apply the Mann-Whitney U test. **')
            # Buscando os labels dos clusters
            cluster_a, cluster_b = valid_clusters

            df_cluster_a = df_cluster[df_cluster['cluster'] == cluster_a]
            df_cluster_b = df_cluster[df_cluster['cluster'] == cluster_b]

            # aplicação do teste de mannwhitney
            mannwhitney_results = {}

            for column in df_cluster.columns[:-1]:  # Excluindo a coluna 'cluster'
                stat, p_value = stats.mannwhitneyu(df_cluster_a[column], df_cluster_b[column])
                mannwhitney_results[column] = {'U statistic': stat, 'p-value': p_value}

            # mostrando os resultados
            df_results = pd.DataFrame(mannwhitney_results).T
            print(f'\nStatistical Results:\n{df_results}')

            # Interpretação
            print("\nInterpretation of Results:")
            for column, values in mannwhitney_results.items():
                p_value = values['p-value']
                if p_value < significance_level:
                    print(f" - {column}: ✨ Significant difference between clusters (p-value={p_value:.4f})")
                else:
                    print(f" - {column}: ✅ No significant difference between clusters (p-value={p_value:.4f})")
                    
        # Teste Kruskal Wallis aplicado quando se tem mais de 2 clusters
        # Em caso de existir significância estatística, aplica-se o teste Dunn para vericar qual cluster tem melhor resultado
        elif len(valid_clusters)>2:
            print(f'** More than two clusters were found; therefore, we will apply the Kruskal-Wallis test and the Dunn test. **')

            # Contador para verificar qual cluster aparece com mais frequência em diferenças significativas
            difference_counter = defaultdict(int)

            # Filtrar clusters válidos (removendo -1 se presente)
            valid_clusters = [cluster for cluster in df_cluster["cluster"].unique() if cluster != -1]

            for feature in df_cluster.columns[:-1]:  # Excluding the 'cluster' column
                print(f"\n🔹 Testing attribute: {feature}")

                # Separação dos clusters
                groups = [df_cluster[df_cluster["cluster"] == cluster][feature] for cluster in valid_clusters]

                # Fase 1: Kruskal-Wallis Test
                stat, p = stats.kruskal(*groups)
                print(f"   - H Statistic = {stat:.4f}, p-value = {p:.4f}")

                # Se existir diferença estatísticamente significante, ou seja, valor p menor que o nível de significância, aplica´se o teste Dunn
                if p < significance_level:
                    print("   ✨ Statistically significant difference found! Applying Dunn's test...")

                    # Fase 2: Teste de Dunn para comparações múltiplas (apenas clusters válidos)
                    df_filtered = df_cluster[df_cluster["cluster"].isin(valid_clusters)]
                    dunn_results = sp.posthoc_dunn(df_filtered, val_col=feature, group_col='cluster', p_adjust='bonferroni')

                    print("   🔍 Dunn's Test Results (adjusted p-values):")
                    print(dunn_results)

                    # Contando com que frequência cada cluster aparece em diferenças significativas
                    for i, row in enumerate(dunn_results.index):
                        for j, col in enumerate(dunn_results.columns):
                            if i < j:  # Evita comparações duplicadas
                                p_dunn = dunn_results.loc[row, col]
                                if p_dunn < significance_level:
                                    print(f"    Cluster {row} is significantly different from Cluster {col} (p = {p_dunn:.4f})")
                                    difference_counter[row] += 1
                                    difference_counter[col] += 1
                else:
                    print("   ✅ No significant differences between clusters for this feature.")

            # Exibindo os clusters mais frequentemente encontrados como diferentes
            print("\n📊 **Summary: Clusters that appeared most frequently as different**")
            sorted_clusters = sorted(difference_counter.items(), key=lambda x: x[1], reverse=True)
            for cluster, count in sorted_clusters:
                print(f"   - Cluster {cluster}: {count} occurrences of significant difference")
        else: 
            print("❌ Error: At least two clusters are required to perform a statistical significance test.")

    #MÉTODO_5 -> Realiza a checagem de algum cluster com Perfil SRL segundo as definições do nosso projeto
    # Cluster com maiores médias e mediannas nos atributos são considerados com Perfil SRL, para agrupamento com mais de 2 clusters é feito um rankeamento
    def checkProfileSRL(self, dataframe):
        df_cluster = self.removeIdentifierColumns(dataframe)
        significance_level = 0.05

        unique_clusters = df_cluster["cluster"].unique()
        valid_clusters = [c for c in unique_clusters if c != -1]

        higher_mean_counter = defaultdict(int)
        cluster_stats = {}

        #2 clusters
        if len(valid_clusters) == 2:
            cluster_a, cluster_b = valid_clusters
            df_cluster_a = df_cluster[df_cluster['cluster'] == cluster_a]
            df_cluster_b = df_cluster[df_cluster['cluster'] == cluster_b]

            for column in df_cluster.columns[:-1]:  # Excluindo 'cluster'
                stat, p_value = mannwhitneyu(df_cluster_a[column], df_cluster_b[column])

                if p_value < significance_level:
                    mean_a, mean_b = df_cluster_a[column].mean(), df_cluster_b[column].mean()
                    significant_cluster = cluster_a if mean_a > mean_b else cluster_b
                    higher_mean_counter[significant_cluster] += 1

            # Salvar estatísticas de cada cluster
            for cluster in valid_clusters:
                cluster_stats[cluster] = {
                    "mean": df_cluster[df_cluster["cluster"] == cluster].mean(),
                    "median": df_cluster[df_cluster["cluster"] == cluster].median()
                }
        # Mais de 2 clusters
        elif len(valid_clusters) > 2:
            difference_counter = defaultdict(int)

            for feature in df_cluster.columns[:-1]:  # Excluindo 'cluster' -1 (Outliers)
                groups = [df_cluster[df_cluster["cluster"] == cluster][feature] for cluster in valid_clusters]

                stat, p = kruskal(*groups)

                if p < significance_level:
                    df_filtered = df_cluster[df_cluster["cluster"].isin(valid_clusters)]
                    dunn_results = sp.posthoc_dunn(df_filtered, val_col=feature, group_col='cluster', p_adjust='bonferroni')

                    for i, row in enumerate(dunn_results.index):
                        for j, col in enumerate(dunn_results.columns):
                            if i < j and dunn_results.loc[row, col] < significance_level:
                                mean_row = df_cluster[df_cluster["cluster"] == row][feature].mean()
                                mean_col = df_cluster[df_cluster["cluster"] == col][feature].mean()
                                significant_cluster = row if mean_row > mean_col else col
                                higher_mean_counter[significant_cluster] += 1

            # Salvar estatísticas de cada cluster
            for cluster in valid_clusters:
                cluster_stats[cluster] = {
                    "mean": df_cluster[df_cluster["cluster"] == cluster].mean(),
                    "median": df_cluster[df_cluster["cluster"] == cluster].median()
                }

        else:
            print("❌ Error: At least two clusters are required to perform a statistical significance test.")
            return

        # 🏆 Garantir que todos os clusters estejam no ranking
        all_clusters = set(valid_clusters)  # Todos os clusters
        ranked_clusters = set(higher_mean_counter.keys())  # Apenas os que tiveram alguma média maior que os demais

        # Encontrar os clusters que nunca alcançaram média maior em algum atributo (devem estar na última posição)
        non_ranked_clusters = list(all_clusters - ranked_clusters)

        # Lista de clusters ordenada pelo número de vezes que tiveram algum atributo com média maior que os demais
        sorted_clusters = sorted(higher_mean_counter.items(), key=lambda x: x[1], reverse=True)
        cluster_ranking = [cluster for cluster, _ in sorted_clusters]

        # Adicionar os clusters que nunca tiveram média maior ao final da lista
        cluster_ranking.extend(non_ranked_clusters)

        # Exibindo médias e medianas de cada cluster antes da definição do perfil SRL
        print("\n**Mean and Median Values by Cluster**")
        for cluster, stats in cluster_stats.items():
            print(f"\nCluster {cluster}:")
            print(f"   - Mean:\n{stats['mean']}")
            print(f"   - Median:\n{stats['median']}")

        # 🏆 Exibir a hierarquia dos clusters (SRL e demais)
        print("\n **Final Cluster Ranking (From SRL to Lowest)**")
        if len(cluster_ranking) == 2:
            print(f"   1. Cluster {cluster_ranking[0]} → SRL Profile")
            print(f"   2. Cluster {cluster_ranking[1]} → No SRL Profile")
        else:
            for position, cluster in enumerate(cluster_ranking, start=1):
                if position == 1:
                    label = "SRL Profile"
                elif position == len(cluster_ranking):
                    label = "No SRL Profile"
                else:
                    label = f"SRL Profile - Level {position}"
                print(f"   {position}. Cluster {cluster} → {label}")
        
    #MÉTODO_6 -> Método para mostrar a descrição dos clusters segundo a definição de SRL Profile
    # Neste método são consideradas as notas em forma de conceito A, B e C de acordo com a definição do artigos e tese
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
        df2 = df2.fillna('C')  # Substituir NaN por 
        
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
            if(cluster==-1):
                print(f"\nPercentage of Students considered Outliers:")
            else:
                print(f"\nPercentage of Students in the Cluster {cluster}:")
            print(f"   Students with A Status = {a_count} ({a_pct:.2f}%)")
            print(f"   Students with B Status = {b_count} ({b_pct:.2f}%)")
            print(f"   Students with C Status = {c_count} ({c_pct:.2f}%)")
            print("-"*40)

    #MÉTODO_7 --> Método para destacar a descrição dos perfis SRL em formato de gráfico de barras
    def profileSRLGraphics(self, dataframe, fileGrade, separatorFileGrade, path, show_outliers=True):
        dfGrade = pd.read_csv(fileGrade, delimiter=separatorFileGrade)

        # Caso a coluna grade seja do tipo object, converte "9,6" para "9.6"
        if dfGrade["grade"].dtype == object:
            dfGrade["grade"] = dfGrade["grade"].str.replace(",", ".", regex=False)

        if not pd.api.types.is_numeric_dtype(dfGrade["grade"]):
            dfGrade["grade"] = pd.to_numeric(dfGrade["grade"], errors='coerce')

        dfGrade["status"] = dfGrade["grade"].apply(lambda x: "C" if x < 6 else ("B" if x < 8 else "A"))

        df2 = dataframe.merge(dfGrade[['iduser', 'status']], on='iduser', how='left')
        df2 = df2.fillna('C')

        # Filtrar outliers caso solicitado
        if not show_outliers:
            if -1 in df2['cluster'].values:
                df2 = df2[df2['cluster'] != -1]

        concept_counts = df2.groupby(['cluster', 'status']).size().unstack(fill_value=0)
        concept_percentages = concept_counts.div(concept_counts.sum(axis=1), axis=0) * 100

        colors = ['#1f77b4', '#aec7e8', '#ffbb78']

        ax = concept_percentages.plot(kind='barh', stacked=True, figsize=(10, 6), color=colors)

        for i, (index, row) in enumerate(concept_percentages.iterrows()):
            cumulative_width = 0
            for j, value in enumerate(row):
                if value > 0:
                    ax.text(
                        cumulative_width + value / 2,
                        i,
                        f'{value:.1f}%',
                        va='center', ha='center', fontsize=9, color='black'
                    )
                    cumulative_width += value

        plt.xlabel('Percentage (%)')
        plt.ylabel('Cluster')
        plt.yticks(rotation=0)
        plt.legend(title='Grade')
        plt.grid(axis='x', linestyle='--', alpha=0.7)

        plt.savefig(path + self.algorithm + '_profileSRL.png')
        print(f'Profile SRL Graphic for {self.algorithm} algorithm saved in {path}')
        plt.show()

    #MÉTODO_8 -> Método para criar vários tipos de gráficos de comparação dos cluster por atributos 
    def plotGraphicClusters(self, dataframe, rows, columns, type_graphic, path, show_outliers=True):
       
        numeric_columns = dataframe.columns[1:-1]

        # Criar novo DataFrame sem colunas desnecessárias
        if 'iduser' in dataframe.columns:
            df_cluster = dataframe.drop(columns=['iduser'])
        else:
            df_cluster = dataframe

        # Filtrar outliers se solicitado
        if not show_outliers:
            if -1 in df_cluster['cluster'].values:
                df_cluster = df_cluster[df_cluster['cluster'] != -1]

        # Garantir que apenas as colunas numéricas sejam usadas, excluindo 'cluster'
        list_columns = [col for col in df_cluster.columns if col != 'cluster']

        plt.figure(figsize=(16, 8))
        num_subplots = len(list_columns)

        for i, col in enumerate(list_columns, 1):
            plt.subplot(rows, columns, i)

            if type_graphic == 'boxplot':
                sns.boxplot(x='cluster', y=col, data=df_cluster, hue='cluster', palette="Set2", legend=False)
            elif type_graphic == 'violinplot':
                sns.violinplot(x='cluster', y=col, data=df_cluster, hue='cluster', palette="Set2", legend=False)
            elif type_graphic == 'stripplot':
                sns.stripplot(x='cluster', y=col, data=df_cluster, hue='cluster', palette="Set2", legend=False)
            elif type_graphic == 'density':
                sns.kdeplot(data=df_cluster, x=col, hue='cluster', fill=True, common_norm=False, palette="Set2")
            else:
                print('Unsupported chart type!\nChoose: boxplot, violinplot, stripplot or density to generate the plot')

            plt.title(col)

        plt.tight_layout()
        plt.savefig(path + self.algorithm + type_graphic + '.png')
        print(f'{type_graphic} for {self.algorithm} algorithm saved in {path}')
        plt.show()
