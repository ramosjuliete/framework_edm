# Documentação Técnica — MinimalDataset (com exemplos práticos)

A classe **`MinimalDataset`** processa logs educacionais da plataforma Moodle, filtrando-os por estudantes, quantificando eventos,
mapeando-os para estratégias de autorregulação da aprendizagem (SRL) e unindo com dados de tempo para gerar um minimal dataset final pronto para aplicação de algoritmos de agrupamento de dados.


## Sumário
- [Visão geral](#visão-geral)
- [Instalação e pré-requisitos](#instalação-e-pré-requisitos)
- [Fluxo recomendado](#fluxo-recomendado)
- [API da classe](#api-da-classe)
  - [`__init__(generation_method)`](#__initgeneration_method)
  - [`extract_id_user(description)`](#extract_id_userdescription)
  - [`logfilltering(...)`](#logfilltering)
  - [`log_analysis(...)`](#log_analysis)
  - [`mappingToSRL(dataframe, fileDescriptionSRL, delFileDescriptionSRL)`](#mappingtosrl)
  - [`converToSeconds(tempo_str)`](#convertoseconds)
  - [`joinTime(fileTime, delimitterFileTime, dataframe)`](#jointime)
  - [`structureTime(...)`](#structuretime)
  - [`generateSRLFileMap(path, df_srl, df_logs)`](#generatesrlfilemap)
  - [`generateMinimalDataset(path, dataframe)`](#generateminimaldataset)
- [Exemplo de ponta-a-ponta](#exemplo-de-ponta-a-ponta)
- [Boas práticas e validações](#boas-práticas-e-validações)

## Visão geral
A classe recebe um **`generation_method`** que ajusta o comportamento para diferentes origens de dados (ex.: `SQL`, `MOODLE`, `MOODLE_PYTHON`).

## Instalação e pré-requisitos
```bash
pip install pandas
```

Estrutura de arquivos típica usada nos exemplos:
```
data/
  logs.csv
  students.csv
  srl_map.csv
  tempus.csv        # tabela com tempos por usuário
out/
  # arquivos gerados serão salvos aqui
```

## Fluxo recomendado
1. **Filtrar logs** por estudantes: `logfilltering(...)`
2. **Quantificar eventos** por usuário: `log_analysis(...)`
3. **Mapear eventos** para SRL: `mappingToSRL(...)`
4. **Tratar/Unir tempos**: `structureTime(...)` e/ou `joinTime(...)`
5. **Gerar dataset final**: `generateMinimalDataset(...)`

---

## API da classe

### `__init__(generation_method)`
- **Parâmetros**: `generation_method: str` (ex.: `"SQL"`, `"MOODLE"`, `"MOODLE_PYTHON"`)
- **Exemplo**:
```python
from minimaldataset import MinimalDataset
mds = MinimalDataset(generation_method="MOODLE")
```

### `extract_id_user(description)`
Extrai o ID de usuário contido em uma descrição com padrão como: `user with id '123'`.

- **Parâmetros**: `description: str`
- **Retorno**: `str | None`
- **Exemplo**:
```python
desc = "The event was triggered by user with id '987' in course 'ABC'."
uid = mds.extract_id_user(desc)  # "987"
```

### `logfilltering(...)`
Filtra o CSV de logs mantendo apenas registros de **estudantes**.

- **Parâmetros (típicos)**:
  - `fileLogs: str` — caminho do CSV de logs
  - `fileLogsDelimiter: str` — delimitador, ex.: `","` ou `";"`
  - `columnGeneral: str` — coluna de identificação do usuário (ex.: nome completo)
  - `columnDescription: str` — coluna com a descrição do evento
  - `fileStudents: str` — caminho do CSV com a lista de estudantes
  - `columnFilter: str` — coluna do CSV de estudantes usada para filtrar (ex.: `fullname`)
  - `logPathDestination: str` — diretório de saída (ex.: `"out/"`)

- **Exemplo**:
```python
mds.logfilltering(
    fileLogs="data/logs.csv",
    fileLogsDelimiter=",",
    columnGeneral="userfullname",
    columnDescription="description",
    fileStudents="data/students.csv",
    columnFilter="fullname",
    logPathDestination="out/"
)
# Gera algo como: out/logMoodleFiltered.csv
```

### `log_analysis(...)`
Transforma eventos em **colunas** e **contagens** por `iduser` (pivot/crosstab). Pode normalizar nomes ou aplicar mapeamento SRL conforme o `generation_method`.

- **Parâmetros (típicos)**:
  - `fileLogs: str`
  - `fileLogsDelimiter: str`
  - `columnIdentifier: str` — ex.: `"iduser"`
  - `columnLogEvent: str` — ex.: `"event_name"`
  - `fileDescriptionSRL: str | None` — arquivo de mapeamento (quando aplicável)
  - `delFileDescriptionSRL: str` — delimitador do mapeamento (quando aplicável)

- **Retorno**: `pandas.DataFrame`

- **Exemplo**:
```python
df_events = mds.log_analysis(
    fileLogs="out/logMoodleFiltered.csv",
    fileLogsDelimiter=",",
    columnIdentifier="iduser",
    columnLogEvent="event_name",
    fileDescriptionSRL="data/srl_map.csv",
    delFileDescriptionSRL=";"
)
# df_events.head()
```

### `mappingToSRL(dataframe, fileDescriptionSRL, delFileDescriptionSRL)`
Agrega colunas de eventos para **estratégias SRL** conforme um mapa `event_name -> srl_strategy`.

- **Parâmetros**:
  - `dataframe: pandas.DataFrame` (resultado do `log_analysis`)
  - `fileDescriptionSRL: str`
  - `delFileDescriptionSRL: str`

- **Retorno**: `pandas.DataFrame` (com colunas por estratégia SRL)

- **Exemplo**:
```python
df_srl = mds.mappingToSRL(
    dataframe=df_events,
    fileDescriptionSRL="data/srl_map.csv",
    delFileDescriptionSRL=";"
)
# df_srl.head()
```

### `converToSeconds(tempo_str)`
Converte textos como `"2 horas 10 minutos 30 segundos"` para **inteiros em segundos**.

- **Parâmetros**: `tempo_str: str`
- **Retorno**: `int`

- **Exemplo**:
```python
sec = mds.converToSeconds("1 hora 5 minutos 20 segundos")  # 3920
```

### `joinTime(fileTime, delimitterFileTime, dataframe)`
Realiza **merge** do dataframe de eventos com um CSV de **tempos por usuário**.

- **Parâmetros**:
  - `fileTime: str`
  - `delimitterFileTime: str`
  - `dataframe: pandas.DataFrame` (ex.: `df_srl`)

- **Retorno**: `pandas.DataFrame` (com coluna `time` unida)

- **Exemplo**:
```python
df_final = mds.joinTime(
    fileTime="data/tempus.csv",
    delimitterFileTime=";",
    dataframe=df_srl
)
# df_final.head()
```

### `structureTime(...)`
Lê um CSV de tempos da origem (ex.: Moodle) e gera um **arquivo padronizado** com colunas `{{iduser, time}}` (tempo em segundos).

- **Parâmetros (típicos)**:
  - `fileTime: str`
  - `delimitterFileTime: str`
  - `columnUser: str`
  - `columnTime: str`
  - `pathDestination: str`

- **Exemplo**:
```python
mds.structureTime(
    fileTime="data/moodle_time_raw.csv",
    delimitterFileTime=";",
    columnUser="iduser",
    columnTime="duration_str",
    pathDestination="out/"
)
# Gera algo como: out/time_MOODLE.csv
```

### `generateSRLFileMap(path, df_srl, df_logs)`
Gera um CSV de mapeamento SRL **apenas para os eventos existentes** nos logs (útil para iniciar/atualizar o mapa e listar não mapeados).

- **Parâmetros**:
  - `path: str` — diretório de saída
  - `df_srl: pandas.DataFrame` — dataframe do mapa completo (ou carregado de `srl_map.csv`)
  - `df_logs: pandas.DataFrame` — dataframe de logs ou de eventos já pivotado

- **Efeito**: salva `fileSRLMappping<generation_method>.csv` e imprime eventos não mapeados para que o usuário possa incluir no arquivo manualmente (se assim desejar)

- **Exemplo**:
```python
# Supondo df_logs seja um DF com a coluna 'event_name'
mds.generateSRLFileMap(
    path="out/",
    df_srl=df_srl,       # ou um DF carregado de data/srl_map.csv
    df_logs=df_events    # ou outro DF que contenha 'event_name'
)
```

### `generateMinimalDataset(path, dataframe)`
Salva o dataset final com nome `generaldataset_<generation_method>.csv` no caminho indicado.

- **Parâmetros**:
  - `path: str`
  - `dataframe: pandas.DataFrame`

- **Exemplo**:
```python
mds.generateMinimalDataset("out/", df_final)
# out/generaldataset_MOODLE.csv
```

---

## Exemplo de ponta-a-ponta
```python
import pandas as pd
from minimaldataset import MinimalDataset

mds = MinimalDataset(generation_method="MOODLE")

# 1) Filtrar logs por estudantes
mds.logfilltering(
    fileLogs="data/logs.csv", fileLogsDelimiter=",",
    columnGeneral="userfullname", columnDescription="description",
    fileStudents="data/students.csv", columnFilter="fullname",
    logPathDestination="out/"
)

# 2) Analisar/quantificar eventos
df_events = mds.log_analysis(
    fileLogs="out/logMoodleFiltered.csv", fileLogsDelimiter=",",
    columnIdentifier="iduser", columnLogEvent="event_name",
    fileDescriptionSRL="data/srl_map.csv", delFileDescriptionSRL=";"
)

# 3) Mapear para SRL (opcional, caso não tenha sido aplicado no passo 2)
df_srl = mds.mappingToSRL(
    dataframe=df_events,
    fileDescriptionSRL="data/srl_map.csv",
    delFileDescriptionSRL=";"
)

# 4) Estruturar/Unir tempos
mds.structureTime(
    fileTime="data/moodle_time_raw.csv", delimitterFileTime=";",
    columnUser="iduser", columnTime="duration_str", pathDestination="out/"
)

df_final = mds.joinTime(
    fileTime="out/time_MOODLE.csv", delimitterFileTime=";",
    dataframe=df_srl
)

# 5) Gerar dataset final
mds.generateMinimalDataset("out/", df_final)
```

## Boas práticas e validações
- Verifique **nomes de colunas** exatos em cada CSV.
- Normalize `event_name` para evitar duplicidades por variações de maiúsculas/minúsculas e barras.
- Garanta que o **mapa SRL** cubra a maioria dos eventos; use `generateSRLFileMap` para localizar lacunas e se necessário acrescente os logs não mapeados manualmente para garantir que não perca nenhum log.
- Em arquivos de tempo, padronize para **segundos** (use `converToSeconds`) antes de unir.
- Mantenha um **dicionário de eventos** por origem (`SQL`, `MOODLE`) para reprodutibilidade.
