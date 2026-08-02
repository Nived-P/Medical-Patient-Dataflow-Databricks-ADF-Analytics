 ## Databricks workspace:
 - created a databricks workspace in same region
 - creating namespace again as the already existing one was deleted for the pause.
 ## Create a cluster(compute) in databricks:
- Policy: Personal Compute / Single User if available
- Cluster mode: Single Node
- Runtime version: latest LTS
- Node type: smallest available
- Auto-termination: 20-30 minutes — set this without fail
- I have selected 16 GB memory and 4 cores cluster.

## Bronze notebook:
- raw data from azure event hub is moved to bronze layer delta tables where data is stored in bronze container.
- Read the raw binary stream from Event Hub (via Kafka protocol)
- Cast/decode those bytes into a string (typically UTF-8)
- That string is JSON text ,the same JSON structure the simulator script sent (patient_id, gender, age, etc.)
- Write this raw JSON content into Delta tables in bronze container  with minimal transformation, just capturing the raw event as-is, maybe adding an ingestion timestamp.
- Rest of the work in Databricks_notebook.
- import all modules.
- mention the event hub configuration and kafka options.
- read the data from event hub
- cast the value  from kafka binary to json strings.
- mention the adls configuration and bronze path
- Then write json stream into bronze delta table, mention checkpoint location as well.

## notes and tips:

- prepare basic code without actual values in notebook and copy to 01_Bronze_rawdata.py, then duplicate it into 01_Bronze_local_rawdata.py and fill actual values of event hub config,storage account access key.