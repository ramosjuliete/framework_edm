# Documentação Técnica — General (orquestrador do framework)

A classe **General** funciona como um **orquestrador**: recebe um dataset mínimo já processado em `.csv` e executa em sequência as etapas de análise exploratória, clusterização e análise de resultados.

> **Stack assumida nos exemplos:** `pandas`, `scipy`, `scikit-learn`, `matplotlib`

## Sumário
- [Visão geral](#visão-geral)
- [Instalação e pré-requisitos](#instalação-e-pré-requisitos)
- [Fluxo do método execute](#fluxo-do-método-execute)
- [API da classe](#api-da-classe)
- [Exemplo de uso](#exemplo-de-uso)
- [Boas práticas](#boas-práticas)

## Visão geral
- Entrada: dataset mínimo (`minimaldataset.csv`).
- Saída: estatísticas descritivas, clusters, análises de resultados, gráficos e arquivo de resumo (`<path>/<algorithm>_results.txt`).

## Instalação e pré-requisitos
```bash
pip install pandas scipy scikit-learn matplotlib hdbscan
```

## Fluxo do método execute
1. **ExploratoryAnalysis**
   - Carrega dataset
   - Estatísticas descritivas
   - Teste de normalidade (Shapiro, Smirnov ou Anderson)
   - Matriz de correlação Spearman

2. **Clustering**
   - Executa algoritmo escolhido:
     - KMeans → `k`
     - Agglomerative → `n_clusters`
     - Gaussian → `n_clusters`
     - HDBSCAN → `min_samples`, `min_cluster_size`
     - DBSCAN → `value_eps`, `value_minsamples`

3. **ResultsAnalysis**
   - Estatísticas por cluster
   - Testes de significância
   - Perfis SRL (tabelas e gráficos)
   - Exporta resultados

---

## API da classe
### `__init__(fileDataset, delimiterDataset, path)`
**Parâmetros:** `fileDataset, delimiterDataset, path`

**Exemplo:**
```python
g.__init__(fileDataset, delimiterDataset, path)
```

### `execute(algorithm, fileGrade, delimiterGrade, normalityTeste)`
**Parâmetros:** `algorithm, fileGrade, delimiterGrade, normalityTeste`

**Exemplo:**
```python
g.execute(algorithm, fileGrade, delimiterGrade, normalityTeste)
```


---

## Exemplo de uso
```python
from general import General

dataset = "out/minimaldataset.csv"

g = General(fileDataset=dataset, delimiterDataset=";", path="out/")

# Execução com K-Means (k=3)
g.execute(
    algorithm="kmeans",
    normalityTeste="shapiro",
    k=3
)

# Execução com HDBSCAN
g.execute(
    algorithm="hdbscan",
    min_samples=5,
    min_cluster_size=10
)

# Execução com Agglomerative + arquivo de notas
g.execute(
    algorithm="agglomerative",
    n_clusters=3,
    fileGrade="out/grades.csv",
    delimiterGrade=";"
)
```

---

## Boas práticas
- Certifique-se que `minimaldataset.csv` está pronto antes de rodar o orquestrador.
- Verifique o **delimitador** (`;` ou `,`) corretamente.
- Mantenha diretórios separados em `path` para não sobrescrever resultados.
- Inclua colunas esperadas: `iduser`, `time`, `SRL_Planning`, `SRL_Monitoring`, `SRL_Evaluation`, `TotalEvents`.
- Para análises com notas (`fileGrade`), valide consistência da coluna `iduser`.
