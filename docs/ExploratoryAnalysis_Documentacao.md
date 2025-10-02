# Documentação Técnica — ExploratoryAnalysis (com exemplos práticos)

A classe executa análises exploratórias estatísticas em DataFrames, incluindo estatísticas descritivas, testes de normalidade e correlações. 
O padrão de arquivos recebido por essa classe póde ser um dataset gerado pela classe MinimalDataset ou um dataset gerado pelo usuário desde que respeite as denominações de um dataset mínimo para análise exploratória

## Sumário
- [Visão geral](#visão-geral)
- [Instalação e pré-requisitos](#instalação-e-pré-requisitos)
- [Fluxo recomendado](#fluxo-recomendado)
- [API da classe](#api-da-classe)
- [Exemplo de uso (ponta-a-ponta)](#exemplo-de-uso-ponta-a-ponta)
- [Boas práticas](#boas-práticas)

## Visão geral
Esta classe centraliza rotinas de **análise exploratória** para seus datasets de aprendizagem: estatística descritiva, distribuição/normalidade, correlações e gráficos de apoio.

## Instalação e pré-requisitos
```bash
pip install pandas scipy statsmodels matplotlib
```

## Fluxo recomendado
1. **Limpeza/validação** do DataFrame de entrada (`NaN`, tipos numéricos).
2. **Descritivas** (`describe`, métricas de tendência e dispersão).
3. **Normalidade** (Shapiro / Kolmogorov–Smirnov / Anderson-Darling).
4. **Correlação** (Pearson/Spearman conforme normalidade).
5. **Visualizações** (boxplot/histograma/scatter).
6. **Comparações** entre grupos (se aplicável).

---

## API da classe
### `__init__(path_sheet, separator)`
**Parâmetros:** `path_sheet, separator`

**Exemplo:**
```python
# Exemplo usando colunas reais do seu dataset
# Supondo df com colunas: 'iduser', 'time', 'SRL_Planning', 'SRL_Monitoring', 'SRL_Evaluation', 'TotalEvents'
ea.__init__(path_sheet, separator)
```

### `removeIdentifierColumns(dataframe)`
**Parâmetros:** `dataframe`

**Exemplo:**
```python
# Exemplo usando colunas reais do seu dataset
# Supondo df com colunas: 'iduser', 'time', 'SRL_Planning', 'SRL_Monitoring', 'SRL_Evaluation', 'TotalEvents'
ea.removeIdentifierColumns(df)
```

### `loadDataframe()`
**Parâmetros:** `—`

**Exemplo:**
```python
# Exemplo usando colunas reais do seu dataset
# Supondo df com colunas: 'iduser', 'time', 'SRL_Planning', 'SRL_Monitoring', 'SRL_Evaluation', 'TotalEvents'
ea.loadDataframe()
```

### `informationData(dataframe)`
**Parâmetros:** `dataframe`

**Exemplo:**
```python
# Exemplo usando colunas reais do seu dataset
# Supondo df com colunas: 'iduser', 'time', 'SRL_Planning', 'SRL_Monitoring', 'SRL_Evaluation', 'TotalEvents'
ea.informationData(df)
```

### `statisticalDescription(dataframe)`
**Parâmetros:** `dataframe`

**Exemplo:**
```python
# Exemplo usando colunas reais do seu dataset
# Supondo df com colunas: 'iduser', 'time', 'SRL_Planning', 'SRL_Monitoring', 'SRL_Evaluation', 'TotalEvents'
ea.statisticalDescription(df)
```

### `createSpearmanMatrix(dataframe, path)`
**Parâmetros:** `dataframe, path`

**Exemplo:**
```python
# Exemplo usando colunas reais do seu dataset
# Supondo df com colunas: 'iduser', 'time', 'SRL_Planning', 'SRL_Monitoring', 'SRL_Evaluation', 'TotalEvents'
ea.createSpearmanMatrix(df, path)
```

### `shapiro_wilk_test(dataframe)`
**Parâmetros:** `dataframe`

**Exemplo:**
```python
# Exemplo usando colunas reais do seu dataset
# Supondo df com colunas: 'iduser', 'time', 'SRL_Planning', 'SRL_Monitoring', 'SRL_Evaluation', 'TotalEvents'
ea.shapiro_wilk_test(df)
```

### `kolmogorov_smirnov_test(dataframe)`
**Parâmetros:** `dataframe`

**Exemplo:**
```python
# Exemplo usando colunas reais do seu dataset
# Supondo df com colunas: 'iduser', 'time', 'SRL_Planning', 'SRL_Monitoring', 'SRL_Evaluation', 'TotalEvents'
ea.kolmogorov_smirnov_test(df)
```

### `anderson_darling_test(dataframe)`
**Parâmetros:** `dataframe`

**Exemplo:**
```python
# Exemplo usando colunas reais do seu dataset
# Supondo df com colunas: 'iduser', 'time', 'SRL_Planning', 'SRL_Monitoring', 'SRL_Evaluation', 'TotalEvents'
ea.anderson_darling_test(df)
```

### `applyNormalityTest(dataframe, test)`
**Parâmetros:** `dataframe, test`

**Exemplo:**
```python
# Exemplo usando colunas reais do seu dataset
# Supondo df com colunas: 'iduser', 'time', 'SRL_Planning', 'SRL_Monitoring', 'SRL_Evaluation', 'TotalEvents'
# parâmetro test pode receber os valores 'smirnov', 'shapiro' ou 'anderson'
ea.applyNormalityTest(df, test='smirnov')
```


## Exemplo de uso (ponta-a-ponta)

```python
import numpy as np
import pandas as pd
from exploratoryanalysis import ExploratoryAnalysis

# DataFrame com nomes de colunas reais
df = pd.DataFrame({
    "iduser": [1,2,3,4,5,6,7,8,9,10],
    "time": [1200, 850, 930, 4000, 2100, 760, 1800, 3000, 2500, 1100],
    "SRL_Planning": [5,3,4,10,6,2,5,8,7,3],
    "SRL_Monitoring": [4,2,3,9,5,1,4,7,6,2],
    "SRL_Evaluation": [2,1,2,6,3,1,2,5,4,1],
    "TotalEvents": [80, 55, 61, 150, 98, 40, 77, 130, 115, 60]
})

ea = ExploratoryAnalysis()

# 1) Estatísticas descritivas por coluna de interesse
desc = ea.describe(df)
print(desc)

# 2) Testes de normalidade (Shapiro, K-S, Anderson) para 'time' e no dataframe completo, destacando a normalidade de todos os atributos presentes no dataset
norm_time = ea.normality_tests(df, columns=["time"])
norm_completo = ea.normality_tests(df)
print(norm_time)
print(norm_completo)

# 3) Correlação entre todos os atributos do dataset
corr = ea.correlation(df)
print(corr)

```



## Boas práticas
- **Nomes de colunas consistentes**: use `iduser`, `time` (em segundos), `SRL_Planning`, `SRL_Monitoring`, `SRL_Evaluation`, `TotalEvents`.
- **Valores faltantes**: aplique `dropna()` ou imputação antes de testes de normalidade/correlação.
- **Normalidade**: se `p-value < 0.05`, prefira correlação de Spearman e testes não-paramétricos.
- **Visualizações**: fixe um diretório `out/plots` para manter reprodutibilidade.

