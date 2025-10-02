# Documentação Técnica — ResultsAnalysis (com exemplos práticos)

Esta classe executa análises sobre **resultados dos clusters** já obtidos, incluindo estatísticas descritivas,
testes de significância, descrição de perfis SRL e geração de gráficos comparativos.

> **Stack assumida nos exemplos:** `pandas`, `scipy.stats`, `matplotlib`

## Sumário
- [Visão geral](#visão-geral)
- [Instalação e pré-requisitos](#instalação-e-pré-requisitos)
- [Fluxo recomendado](#fluxo-recomendado)
- [API da classe](#api-da-classe)
- [Exemplo de uso (ponta-a-ponta)](#exemplo-de-uso-ponta-a-ponta)
- [Boas práticas](#boas-práticas)

## Visão geral
Recebe DataFrame com clusters atribuídos aos usuários e colunas de interesse. Permite avaliar diferenças estatísticas entre grupos e descrever perfis de autorregulação.

## Instalação e pré-requisitos
```bash
pip install pandas scipy matplotlib
```

## Fluxo recomendado
1. Gerar `df_clusters` após aplicar métodos de clusterização.
2. Calcular estatísticas descritivas por cluster.
3. Realizar testes de significância para verificar diferenças entre grupos.
4. Gerar tabelas/perfis SRL e visualizações de apoio.

---

## API da classe
### `__init__(algorithm, fileCluster, separatorFileCluster)`
**Parâmetros:** `algorithm, fileCluster, separatorFileCluster`

**Exemplo:**
```python
ra.__init__(algorithm, fileCluster, separatorFileCluster)
```

### `loadFile()`
**Parâmetros:** `—`

**Exemplo:**
```python
ra.loadFile()
```

### `removeIdentifierColumns(dataframe)`
**Parâmetros:** `dataframe`

**Exemplo:**
```python
ra.removeIdentifierColumns(df_clusters)
```

### `statisticalByClusters(df)`
**Parâmetros:** `df`

**Exemplo:**
```python
ra.statisticalByClusters(df_clusters)
```

### `statisticalSignificance(dataframe, significance_level)`
**Parâmetros:** `dataframe, significance_level`

**Exemplo:**
```python
ra.statisticalSignificance(df_clusters, significance_level)
```

### `checkProfileSRL(dataframe)`
**Parâmetros:** `dataframe`

**Exemplo:**
```python
ra.checkProfileSRL(df_clusters)
```

### `profileSRLdescription(dataframe, fileGrade, separatorFileGrade)`
**Parâmetros:** `dataframe, fileGrade, separatorFileGrade`

**Exemplo:**
```python
ra.profileSRLdescription(df_clusters, fileGrade, separatorFileGrade)
```

### `profileSRLGraphics(dataframe, fileGrade, separatorFileGrade, path, show_outliers)`
**Parâmetros:** `dataframe, fileGrade, separatorFileGrade, path, show_outliers`

**Exemplo:**
```python
ra.profileSRLGraphics(df_clusters, fileGrade, separatorFileGrade, "out/", show_outliers)
```

### `plotGraphicClusters(dataframe, rows, columns, type_graphic, path, show_outliers)`
**Parâmetros:** `dataframe, rows, columns, type_graphic, path, show_outliers`

**Exemplo:**
```python
ra.plotGraphicClusters(df_clusters, rows, columns, type_graphic, "out/", show_outliers)
```



## Exemplo de uso (ponta-a-ponta)

```python
import pandas as pd
from resultsanalysis import ResultsAnalysis

# Exemplo de DataFrame clusterizado
df_clusters = pd.DataFrame({
    "iduser": [1,2,3,4,5,6,7,8,9,10],
    "cluster": [0,0,1,1,2,2,0,1,2,0],
    "time": [1200, 850, 930, 4000, 2100, 760, 1800, 3000, 2500, 1100],
    "SRL_Planning": [5,3,4,10,6,2,5,8,7,3],
    "SRL_Monitoring": [4,2,3,9,5,1,4,7,6,2],
    "SRL_Evaluation": [2,1,2,6,3,1,2,5,4,1],
    "TotalEvents": [80,55,61,150,98,40,77,130,115,60],
    "grade": [7.5,6.0,8.0,9.5,5.5,6.5,7.0,8.5,9.0,6.0]
})

ra = ResultsAnalysis(path="out/")

# 1) Estatísticas descritivas por cluster
ra.statisticalByClusters(df_clusters)

# 2) Testes de significância estatística entre clusters
ra.statisticalSignificance(df_clusters)

# 3) Perfil SRL descritivo por cluster
ra.profileSRLdescription(df_clusters)

# 4) Gráficos de perfil SRL por cluster (salvos em disco)
ra.profileSRLGraphics(df_clusters)
```



## Boas práticas
- Use `df_clusters` com colunas: `iduser`, `cluster`, `time`, `SRL_Planning`, `SRL_Monitoring`, `SRL_Evaluation`, `TotalEvents`, `grade`.
- Garanta que `cluster` seja inteiro e não contenha valores nulos.
- Separe bem features de input (SRL/time/events) e variáveis de saída (notas/performance).
- Testes estatísticos assumem certas distribuições; verifique a normalidade antes de escolher paramétricos ou não-paramétricos.

