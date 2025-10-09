# Technical Documentation — MinimalDataset

The **`MinimalDataset`** class processes educational logs from the Moodle platform, filtering them by students, quantifying events, mapping them to self-regulated learning (SRL) strategies, and merging with time data to generate a final minimal dataset ready for clustering algorithms.  

- Input: raw Moodle logs + student list + SRL map + time file  
- Output: CSV file with columns `{iduser, time, SRL_Planning, SRL_Monitoring, SRL_Evaluation, TotalEvents}`  

Main API includes:  
- `logfilltering(...)` → filters student logs  
- `log_analysis(...)` → pivots events into counts  
- `mappingToSRL(...)` → maps events to SRL strategies  
- `converToSeconds(...)` → converts time strings to seconds  
- `joinTime(...)` / `structureTime(...)` → standardizes and merges time data  
- `generateMinimalDataset(...)` → exports the final dataset  

**Best practices:** validate column names, normalize event names, ensure SRL mapping completeness, keep times in seconds.  
