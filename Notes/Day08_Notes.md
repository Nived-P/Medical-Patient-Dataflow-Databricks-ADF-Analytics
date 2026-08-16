# Silver Layer - Data Transformation & Cleaning

## Objective
Transform raw JSON string data from bronze into structured, cleaned data with proper schema, ready for analytics/aggregation in gold layer.

## Process Overview
1. Read streaming data from bronze Delta table
2. Define explicit schema matching source JSON structure
3. Parse JSON string into structured columns
4. Convert string timestamps to proper Timestamp type
5. Clean intentional dirty data (invalid ages, future timestamps)
6. Handle schema evolution defensively
7. Write cleaned, structured data to silver Delta table

## Key Steps

### 1. ADLS Configuration
- Same Key Vault-based authentication pattern as bronze notebook
- Storage account key retrieved via dbutils.secrets.get() - no hardcoded credentials

### 2. Schema Definition
- Used StructType/StructField to explicitly define all 8 fields (patient_id, gender, age, department, admission_time, discharge_time, bed_id, hospital_id)
- admission_time and discharge_time kept as StringType initially (converted to Timestamp explicitly later, since from_json() doesn't reliably auto-detect timestamp formats)

### 3. Reading from Bronze
- Used spark.readStream (not batch read) to continuously process new data as it arrives in bronze
- Maintains end-to-end streaming architecture across all layers

### 4. JSON Parsing
- Used from_json(col("raw_json"), schema) to convert JSON string into a structured "struct" column
- Used .select("data.*") to expand the struct into individual top-level columns
- Result: transformed one raw_json string column into 8 separate, properly typed columns

### 5. Timestamp Conversion
- Applied to_timestamp() to admission_time and discharge_time columns
- Converts string representations into actual Timestamp type, enabling date/time comparisons and calculations

### 6. Data Cleaning Logic

**Invalid admission_time (null or future-dated):**
- Used when().otherwise() conditional logic
- If admission_time is null OR greater than current_timestamp() -> replaced with current_timestamp()
- Otherwise, original value retained
- Design choice: correct/replace invalid values rather than drop rows (preserves record for other valid fields)

**Invalid age (>100):**
- If age > 100 -> replaced with a randomized valid age using floor(rand()*90+1)
- Otherwise, original value retained
- Design choice: used randomization (not a fixed value) to avoid creating an artificial spike/skew in age distribution for later analytics

### 7. Schema Evolution Handling
- Defensive loop checks all expected columns exist in the DataFrame
- Any missing column is added with null values (using lit(None))
- Protects against upstream schema drift breaking the pipeline (production-readiness practice for streaming jobs)

### 8. Write to Silver
- Used writeStream with Delta format, append mode
- Added mergeSchema=true option - allows Delta table to automatically adapt if schema changes slightly, working together with the schema evolution defensive logic above
- Checkpoint location tracks streaming progress for fault tolerance

## Verification
- Confirmed via display(df) in notebook: 151 rows, all columns properly structured and typed
- Confirmed no invalid ages (>100) remaining in output
- Confirmed via Azure Portal: actual .parquet data files present in silver/patient_data container (alongside _checkpoints and _delta_log folders)

## Key Learnings / Interview Talking Points
- Difference between "correcting" vs "dropping" invalid records - a real design tradeoff with no single right answer, depends on business requirements
- Why randomization was used for age cleanup (avoiding distribution skew) vs a fixed fallback for timestamps (less analytically sensitive)
- Schema evolution as a production-readiness concern for streaming pipelines, even when not strictly needed for the current fixed-schema simulator
- Full streaming architecture maintained end-to-end (readStream -> transform -> writeStream), not mixing batch and streaming approaches


