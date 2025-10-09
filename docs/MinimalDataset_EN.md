# Technical Documentation — MinimalDataset (with practical examples)

The **`MinimalDataset`** class processes educational logs from the Moodle platform, filtering them by students, quantifying events, mapping them to self-regulated learning (SRL) strategies, and joining with time data to generate a final minimal dataset ready for applying data clustering algorithms.

## Table of Contents
- [Overview](#overview)
- [Installation & prerequisites](#installation--prerequisites)
- [Recommended workflow](#recommended-workflow)
- [Class API](#class-api)
  - [`__init__(generation_method)`](#__initgeneration_method)
  - [`extract_id_user(description)`](#extract_id_userdescription)
  - [`logfilltering(...)`](#logfilltering)
  - [`log_analysis(...)`](#log_analysis)
  - [`mappingToSRL(dataframe, fileDescriptionSRL, delFileDescriptionSRL)`](#mappingtosrldataframe-filedescriptionsrl-delfiledescriptionsrl)
  - [`converToSeconds(tempo_str)`](#convertoseconds)
  - [`joinTime(fileTime, delimitterFileTime, dataframe)`](#jointimefiletime-delimitterfiletime-dataframe)
  - [`structureTime(...)`](#structuretime)
  - [`generateSRLFileMap(path, df_srl, df_logs)`](#generatesrlfilemappath-df_srl-df_logs)
  - [`generateMinimalDataset(path, dataframe)`](#generateminimaldatasetpath-dataframe)
- [End-to-end example](#end-to-end-example)
- [Best practices and validations](#best-practices-and-validations)

## Overview
The class receives a **`generation_method`** that adjusts behavior for different data sources (e.g., `SQL`, `MOODLE`, `MOODLE_PYTHON`).

## Installation & prerequisites
```bash
pip install pandas
```

Typical file structure used in the examples:
```
data/
  logs.csv
  students.csv
  srl_map.csv
  tempus.csv        # table with times per user
out/
  # generated files will be saved here
```

## Recommended workflow
1. **Filter logs** by students: `logfilltering(...)`
2. **Quantify events** per user: `log_analysis(...)`
3. **Map events** to SRL: `mappingToSRL(...)`
4. **Handle/Join times**: `structureTime(...)` and/or `joinTime(...)`
5. **Generate final dataset**: `generateMinimalDataset(...)`

---

## Class API

### `__init__(generation_method)`
- **Parameters**: `generation_method: str` (e.g., `"SQL"`, `"MOODLE"`, `"MOODLE_PYTHON"`)
- **Example**:
```python
from minimaldataset import MinimalDataset
mds = MinimalDataset(generation_method="MOODLE")
```

### `extract_id_user(description)`
Extracts the user ID contained in a description with a pattern like: `user with id '123'`.

- **Parameters**: `description: str`
- **Return**: `str | None`
- **Example**:
```python
desc = "The event was triggered by user with id '987' in course 'ABC'."
uid = mds.extract_id_user(desc)  # "987"
```

### `logfilltering(...)`
Filters the log CSV keeping only **student** records.

- **Typical parameters**:
  - `fileLogs: str` — path to the log CSV
  - `fileLogsDelimiter: str` — delimiter, e.g., `","` or `";"`
  - `columnGeneral: str` — column for user identification (e.g., full name)
  - `columnDescription: str` — column with the event description
  - `fileStudents: str` — path to the CSV with the list of students
  - `columnFilter: str` — column in the student CSV used for filtering (e.g., `fullname`)
  - `logPathDestination: str` — output directory (e.g., `"out/"`)

- **Example**:
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
# Generates something like: out/logMoodleFiltered.csv
```

### `log_analysis(...)`
Transforms events into **columns** and **counts** by `iduser` (pivot/crosstab). It can normalize names or apply SRL mapping according to the `generation_method`.

- **Typical parameters**:
  - `fileLogs: str`
  - `fileLogsDelimiter: str`
  - `columnIdentifier: str` — e.g., `"iduser"`
  - `columnLogEvent: str` — e.g., `"event_name"`
  - `fileDescriptionSRL: str | None` — mapping file (when applicable)
  - `delFileDescriptionSRL: str` — delimiter of the mapping (when applicable)

- **Return**: `pandas.DataFrame`

- **Example**:
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
Aggregates event columns into **SRL strategies** according to a `event_name -> srl_strategy` map.

- **Parameters**:
  - `dataframe: pandas.DataFrame` (result of `log_analysis`)
  - `fileDescriptionSRL: str`
  - `delFileDescriptionSRL: str`

- **Return**: `pandas.DataFrame` (with columns per SRL strategy)

- **Example**:
```python
df_srl = mds.mappingToSRL(
    dataframe=df_events,
    fileDescriptionSRL="data/srl_map.csv",
    delFileDescriptionSRL=";"
)
# df_srl.head()
```

### `converToSeconds(tempo_str)`
Converts texts like `"2 horas 10 minutos 30 segundos"` to **integers in seconds**.

- **Parameters**: `tempo_str: str`
- **Return**: `int`

- **Example**:
```python
sec = mds.converToSeconds("1 hora 5 minutos 20 segundos")  # 3920
```

### `joinTime(fileTime, delimitterFileTime, dataframe)`
Performs a **merge** of the events dataframe with a CSV containing **time per user**.

- **Parameters**:
  - `fileTime: str`
  - `delimitterFileTime: str`
  - `dataframe: pandas.DataFrame` (e.g., `df_srl`)

- **Return**: `pandas.DataFrame` (with a `time` column joined)

- **Example**:
```python
df_final = mds.joinTime(
    fileTime="data/tempus.csv",
    delimitterFileTime=";",
    dataframe=df_srl
)
# df_final.head()
```

### `structureTime(...)`
Reads a time CSV from the source (e.g., Moodle) and generates a **standardized file** with columns `{{iduser, time}}` (time in seconds).

- **Typical parameters**:
  - `fileTime: str`
  - `delimitterFileTime: str`
  - `columnUser: str`
  - `columnTime: str`
  - `pathDestination: str`

- **Example**:
```python
mds.structureTime(
    fileTime="data/moodle_time_raw.csv",
    delimitterFileTime=";",
    columnUser="iduser",
    columnTime="duration_str",
    pathDestination="out/"
)
# Generates something like: out/time_MOODLE.csv
```

### `generateSRLFileMap(path, df_srl, df_logs)`
Generates an SRL mapping CSV **only for the events present** in the logs (useful to initialize/update the map and list unmapped events).

- **Parameters**:
  - `path: str` — output directory
  - `df_srl: pandas.DataFrame` — dataframe of the full map (or loaded from `srl_map.csv`)
  - `df_logs: pandas.DataFrame` — logs dataframe or already pivoted events dataframe

- **Effect**: saves `fileSRLMappping<generation_method>.csv` and prints unmapped events so that the user can include them in the file manually (if desired)

- **Example**:
```python
# Assuming df_logs is a DF with column 'event_name'
mds.generateSRLFileMap(
    path="out/",
    df_srl=df_srl,       # or a DF loaded from data/srl_map.csv
    df_logs=df_events    # or another DF containing 'event_name'
)
```

### `generateMinimalDataset(path, dataframe)`
Saves the final dataset with the name `generaldataset_<generation_method>.csv` in the given path.

- **Parameters**:
  - `path: str`
  - `dataframe: pandas.DataFrame`

- **Example**:
```python
mds.generateMinimalDataset("out/", df_final)
# out/generaldataset_MOODLE.csv
```

---

## End-to-end example
```python
import pandas as pd
from minimaldataset import MinimalDataset

mds = MinimalDataset(generation_method="MOODLE")

# 1) Filter logs by students
mds.logfilltering(
    fileLogs="data/logs.csv", fileLogsDelimiter=",",
    columnGeneral="userfullname", columnDescription="description",
    fileStudents="data/students.csv", columnFilter="fullname",
    logPathDestination="out/"
)

# 2) Analyze/quantify events
df_events = mds.log_analysis(
    fileLogs="out/logMoodleFiltered.csv", fileLogsDelimiter=",",
    columnIdentifier="iduser", columnLogEvent="event_name",
    fileDescriptionSRL="data/srl_map.csv", delFileDescriptionSRL=";"
)

# 3) Map to SRL (optional, in case it was not applied in step 2)
df_srl = mds.mappingToSRL(
    dataframe=df_events,
    fileDescriptionSRL="data/srl_map.csv",
    delFileDescriptionSRL=";"
)

# 4) Structure/Join times
mds.structureTime(
    fileTime="data/moodle_time_raw.csv", delimitterFileTime=";",
    columnUser="iduser", columnTime="duration_str", pathDestination="out/"
)

df_final = mds.joinTime(
    fileTime="out/time_MOODLE.csv", delimitterFileTime=";",
    dataframe=df_srl
)

# 5) Generate final dataset
mds.generateMinimalDataset("out/", df_final)
```

## Best practices and validations
- Check **exact column names** in each CSV.
- Normalize `event_name` to avoid duplicates due to case and slash variations.
- Ensure the **SRL map** covers most events; use `generateSRLFileMap` to locate gaps and, if necessary, add unmapped logs manually to ensure you don't miss any log.
- In time files, standardize to **seconds** (use `converToSeconds`) before joining.
- Maintain an **event dictionary** per source (`SQL`, `MOODLE`) for reproducibility.
