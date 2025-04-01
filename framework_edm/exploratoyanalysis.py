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

    def loadDataframe(self):
        df = pd.read_csv(self.path_sheet, delimiter=self.separator)
        return df

    def informationData(self, dataframe):
        return dataframe.info()

    def statisticalDescription(self, dataframe):
        if 'name' in dataframe.columns:
            dataframe.drop('name', axis=1, inplace=True)
        return dataframe.describe()
    
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
    
    # Função para aplicar o teste Kolmogorov-Smirnov
    def aplicar_kstest(self, coluna):
        estatistica, p_valor = kstest(coluna, 'norm')
        return estatistica, p_valor

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
