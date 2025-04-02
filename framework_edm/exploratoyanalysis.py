import pandas as pd
import numpy as np
from scipy import stats
import os
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import kstest

class ExploratoryAnalysis:
    def __init__(self,path_sheet, separator):
        self.path_sheet = path_sheet
        self.separator = separator


    #MÉTODO 1 -> Carregando o dataframe a partir do arquivo enviano no momento da criação do objeto (construtor)
    def loadDataframe(self):
        df = pd.read_csv(self.path_sheet, delimiter=self.separator)
        return df

    #MÉTODO 2 -> Retornando informações do dataframe
    def informationData(self, dataframe):
        return dataframe.info()

    #MÉTODO 3 -> Retornando descrições estatísticas do dataframe
    def statisticalDescription(self, dataframe):
        if 'name' in dataframe.columns:
            dataframe.drop('name', axis=1, inplace=True)
        return dataframe.describe()
    
    #MÉTODO 4 -> Criando a matriz de correlação de Spearman -> quando os dados nao seguem uma distribuição normal
    def createSpearmanMatrix(self, dataframe, path):
        # Colunas a remover
        remove_columns = ['iduser', 'name']
        # Verifica e remove as colunas existentes
        existing_columns = [col for col in remove_columns if col in dataframe.columns]
        if existing_columns:
            dataframe = dataframe.drop(columns=existing_columns)

        # Calcula a matriz de correlação utilizando o método Spearman
        corr = dataframe.corr(method='spearman')
    
        # Configuração do estilo (apenas para visualização em Jupyter ou exportação em HTML)
        styled_corr = corr.style.background_gradient(cmap='coolwarm')
    
        # Criação do heatmap com ajuste de layout
        plt.figure(figsize=(10, 6))
        ax = sns.heatmap(corr, annot=True, cmap='coolwarm', center=0)
        ax.set_title('Spearman Correlation Matrix', fontsize=16)
        plt.tight_layout()
        plt.savefig(path+'spearman_correlation_matrix.png')
        print(f'Spearman Correlation Matrix saved in {path}')
        plt.show()
    

    # MÉTODO 5 -> Aplica o teste de normalidade de dados do Kolmogorov Smirnov
    # Ideal para amostras acima de 5000 registros
    
    def aplicar_kstest(self, coluna):
        estatistica, p_valor = kstest(coluna, 'norm')
        return estatistica, p_valor

    # MÉTODO 6 -> Faz a chamada do teste de normalidade 
    # Para dados abaixo de 5000 --> aplicar Shapiro Wilk (verificar se não preciso implementar este), talvez passar por parametro "shapiro", "smirnov" e "anderson" para escolha um dos testes
    def applyNormalityTest(self, dataframe):
        #if 'iduser' in dataframe.columns:
            #dataframe.drop('iduser', axis=1, inplace=True)
        resultados = {}
        for coluna in dataframe.select_dtypes(include=[np.number]).columns:
            estatistica, p_valor = self.aplicar_kstest(dataframe[coluna])
            resultados[coluna] = {'estatistica': estatistica, 'p_valor': p_valor}

        print(f"\n******************* Results of Kolmogorov-Smirnov Test *******************\n")
    
        for coluna, resultado in resultados.items():
            estatistica = resultado['estatistica']
            p_valor = resultado['p_valor']
            #print(f"{coluna}: statistic = {estatistica}, p_value = {p_valor:.6f}")
            #TROCAR PELAS LINHAS ABAIXO PARA MOSTRAR A FRASE DE NORMALIDADE
            normality = "Follows a normal distribution" if p_valor > 0.05 else "Does not follow a normal distribution"
            print(f"{coluna}: statistic = {estatistica}, p_value = {p_valor:.6f} → {normality}")
        print('\n')
