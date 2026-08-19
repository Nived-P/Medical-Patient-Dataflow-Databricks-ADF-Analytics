# Gold Layer - Star Schema & Dimensional Modeling

## Objective
Transform cleaned silver data into an analytics-ready star schema, with two dimension tables and one fact table, implementing SCD Type 2 on the patient dimension where historical tracking is meaningful.

## Architecture Decision: Star Schema
- Dimension tables (dim_patient, dim_department) store descriptive attributes, one row per entity
- Fact table (fact_admissions) stores measurable events, referencing dimensions via surrogate keys
- Standard data warehousing pattern - optimizes for analytics/BI queries, avoids repeating descriptive data across every event row

## Read Pattern: Batch, not Streaming
- Unlike bronze/silver (which use readStream/writeStream), gold layer uses spark.read (batch)
- Reason: Delta MERGE operations (needed for SCD2) are not well suited to continuous streaming; gold processing is typically run as a scheduled/triggered batch job (e.g., via ADF), while bronze/silver remain continuous

## Dimension 1: dim_patient (Full SCD Type 2)

### Why SCD2 here
Patient attributes (gender, age) could theoretically change over time; SCD2 preserves history rather than overwriting, enabling "what was true as of date X" queries.

### Process
1. Deduplicate silver data to latest admission per patient (using Window + row_number())
2. Select patient_id, gender, age; add effective_from timestamp
3. First run: initialize table with surrogate_key, effective_to=null, is_current=true
4. Subsequent runs:
   - Compute SHA-256 hash of (gender, age) for both incoming and existing target data - used as a fast, single-column way to detect if attributes changed
   - Identify records where hash differs (change detected) -> use DeltaTable.update() to close out old version: set is_current=false, effective_to=current_timestamp()
   - Identify new/changed records (via LEFT JOIN + hash comparison) -> insert fresh version with new surrogate_key, is_current=true, effective_to=null

### Key columns
surrogate_key, patient_id, gender, age, effective_from, effective_to, is_current

## Dimension 2: dim_department (Simple, full refresh - no SCD2)

### Why NOT SCD2 here
Department/hospital combinations are a small (max 49), relatively static reference list. Full overwrite each run is simpler and sufficient - applying SCD2 here would be unnecessary complexity. Good example of applying the right level of complexity per use case, not uniformly.

### Process
1. Select department, hospital_id from silver
2. Deduplicate (dropDuplicates on department + hospital_id combination)
3. Assign surrogate_key
4. Write with mode("overwrite") - full table refresh every run, no incremental logic

### Key columns
surrogate_key, department, hospital_id

## Fact Table: fact_admissions

### Process
1. Read both dimension tables:
   - dim_patient filtered to is_current=true only (get current version)
   - dim_department (no filter needed, always fully current)
2. Build base fact from silver: patient_id, department, hospital_id, admission_time, discharge_time, bed_id
3. Add admission_date (date-only extraction from admission_time) - supports date-based partitioning and aggregation
4. LEFT JOIN to both dimensions to bring in surrogate keys (patient_sk, department_sk) - left join ensures no fact rows are dropped even if a dimension match is missing
5. Compute derived business metrics:
   - length_of_stay_hours: (discharge_time - admission_time) converted to hours via unix_timestamp difference
   - is_currently_admitted: boolean flag, true if discharge_time is still in the future
   - event_ingestion_time: audit timestamp of when this gold record was processed
6. Final column selection: fact_id (own primary key), patient_sk, department_sk, admission_time, discharge_time, admission_date, length_of_stay_hours, is_currently_admitted, bed_id, event_ingestion_time
7. Write with mode("overwrite"), partitioned by admission_date - partitioning improves query performance for date-range filters (common in analytics), even though not critical yet at current small data volume

## Verification
- Patient dim count: 151 (matches silver row count - expected since simulator generates unique UUIDs per event, so no real SCD2 "update" scenarios occur with this synthetic data, only inserts)
- Department dim count: 46 (out of max possible 49 combinations - reasonable given random generation)
- Fact rows: 151 (matches exactly, one fact per admission event)

## Key Learnings / Interview Talking Points
- Star schema fundamentals: dimensions (descriptive, "who/what/where") vs facts (transactional/measurable, "what happened")
- SCD Type 2 mechanics: hash-based change detection, closing out old versions vs inserting new ones, effective_from/effective_to/is_current pattern
- Design judgment: applying SCD2 selectively (patient dimension) rather than universally (department dimension) - matching complexity to actual business need
- Why gold layer often shifts from streaming to batch processing, particularly when MERGE/upsert logic is involved
- Partitioning strategy for fact tables to optimize downstream analytical query performance
- Derived/computed metrics (length_of_stay_hours, is_currently_admitted) as the core value-add of gold layer - transforming raw events into directly consumable business insights