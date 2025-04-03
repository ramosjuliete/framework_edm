import pandas as pd
import numpy as np
from scipy import stats
import os
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import kstest
import scipy.stats as stats

class ExploratoryAnalysis:
    def __init__(self,path_sheet, separator):
        self.path_sheet = path_sheet
        self.separator = separator

    #MÉTODO 1 -> Remove identificadores se houver
    def removeIdentifierColumns(self, dataframe):
        # Colunas a remover
        remove_columns = ['iduser','name']
        # Verifica e remove as colunas existentes
        existing_columns = [col for col in remove_columns if col in dataframe.columns]
        if existing_columns:
            dataframe = dataframe.drop(columns=existing_columns)
        return dataframe

    #MÉTODO 2 -> Carregando o dataframe a partir do arquivo enviano no momento da criação do objeto (construtor)
    def loadDataframe(self):
        df = pd.read_csv(self.path_sheet, delimiter=self.separator)
        return df

    #MÉTODO 3 -> Retornando informações do dataframe
    def informationData(self, dataframe):
        return dataframe.info()

    #MÉTODO 4 -> Retornando descrições estatísticas do dataframe
    def statisticalDescription(self, dataframe):
        if 'name' in dataframe.columns:
            dataframe.drop('name', axis=1, inplace=True)
        return dataframe.describe()
    
    #MÉTODO 5 -> Criando a matriz de correlação de Spearman -> quando os dados nao seguem uma distribuição normal
    def createSpearmanMatrix(self, dataframe, path):

        df = self.removeIdentifierColumns(dataframe)

        # Calcula a matriz de correlação utilizando o método Spearman
        corr = df.corr(method='spearman')
    
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
    

    # MÉTODO 6 -> Aplica o teste de normalidade de dados do Shapiro Wilk - Ideal para dados com até 5000 amostras
    def shapiro_wilk_test(self, dataframe):
        results = []
        for column in dataframe.columns:
            stat, p_value = stats.shapiro(dataframe[column])
            normal = "✅ Yes" if p_value > 0.05 else "❌ Not"
            results.append([column, stat, p_value, normal])
        return pd.DataFrame(results, columns=["Attribute", "Statistic", "p-value", "Normal Distribution?"])

    # MÉTODO 7 -> Aplica o teste de normalidade de dados do Kolmogorov Smirnov 
    def kolmogorov_smirnov_test(self, dataframe):
        results = []
        for column in dataframe.columns:
            stat, p_value = stats.kstest(dataframe[column], 'norm')
            normal = "✅ Yes" if p_value > 0.05 else "❌ Not"
            results.append([column, stat, p_value, normal])
        return pd.DataFrame(results, columns=["Attribute", "Statistic", "p-value", "Normal Distribution?"])

    # MÉTODO 8 -> Aplica o teste de normalidade de dados do Anderson-Darling
    def anderson_darling_test(self, dataframe):
        results = []
        for column in dataframe.columns:
            test_result = stats.anderson(dataframe[column], dist='norm')
            stat = test_result.statistic
            critical_value = test_result.critical_values[2]  # Pegando o valor crítico para 5%
            normal = "✅ Yes" if stat < critical_value else "❌ Not"
            results.append([column, stat, critical_value, normal])
        return pd.DataFrame(results, columns=["Variable", "Statistic", "Critical Value (5%)", "Normal Distribution?"])
   
    # MÉTODO 7 -> Faz a chamada do teste de normalidade que o usuário passar por parâmetro (smirnov, shapiro ou anderson) 
    def applyNormalityTest(self, dataframe, test):
        df = self.removeIdentifierColumns(dataframe)
        df_result = pd.DataFrame()
        if(test=='smirnov'):
            df_result = self.kolmogorov_smirnov_test(df)
            print(f"\n******************* Results of Kolmogorov-Smirnov Test *******************\n")
        elif(test=='shapiro'):
            df_result = self.shapiro_wilk_test(df)
            print(f"\n******************* Results of Shapiro-Wilk Test *******************\n")
        elif(test=='anderson'):
            df_result = self.anderson_darling_test(df)
            print(f"\n******************* Results of Anderson-Darling Test *******************\n")
        else:
            print(f'Error. Test not available!')
            return
        print(df_result)