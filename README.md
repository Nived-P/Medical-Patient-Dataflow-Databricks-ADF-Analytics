# Medical Patient Dataflow — Databricks + ADF Analytics
![Azure](https://img.shields.io/badge/Azure-0089D6?style=flat&logo=microsoft-azure&logoColor=white)
![Databricks](https://img.shields.io/badge/Databricks-FF3621?style=flat&logo=databricks&logoColor=white)
![ADF](https://img.shields.io/badge/Azure_Data_Factory-0078D4?style=flat&logo=microsoft-azure&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Delta Lake](https://img.shields.io/badge/Delta_Lake-003366?style=flat&logoColor=white)
## Project Overview

An end-to-end real-time data engineering pipeline built on Azure, demonstrating a full medallion architecture (Bronze → Silver → Gold) for hospital patient data. The pipeline streams synthetic patient events, processes them through structured transformation layers using PySpark on Databricks, and orchestrates the flow using Azure Data Factory — with all credentials secured via Azure Key Vault.

Built as a portfolio project to demonstrate hands-on Azure Data Engineering skills, including real-world infrastructure troubleshooting encountered throughout development.

## Architecture
## Tech Stack

| Layer | Technology |
|---|---|
| Streaming Ingestion | Azure Event Hub (Standard), azure-eventhub SDK |
| Processing | Azure Databricks (Premium), PySpark, Spark Structured Streaming |
| Storage | ADLS Gen2 (Delta Lake format) |
| Orchestration | Azure Data Factory |
| Security | Azure Key Vault (no hardcoded credentials anywhere) |
| Language | Python 3.x, PySpark |
| Version Control | Git, GitHub |


Local Python Simulator
        │
        ▼
Azure Event Hub (Standard)
        │  Kafka-compatible endpoint
        ▼
Databricks — Bronze Layer
  • Spark Structured Streaming
  • Raw JSON → Delta Lake (ADLS Gen2)
        │
        ▼
Databricks — Silver Layer
  • Schema enforcement + JSON parsing
  • Dirty data cleaning (invalid ages, future timestamps)
  • Schema evolution handling
        │
        ▼
Databricks — Gold Layer
  • Star Schema: dim_patient (SCD Type 2), dim_department, fact_admissions
  • Computed metrics: length_of_stay_hours, is_currently_admitted
        │
        ▼
Azure Data Factory
  • Event-driven orchestration
  • Checks silver row count → conditionally triggers gold notebook
  • 5-minute schedule trigger

## Repository structure
Medical-Patient-Dataflow-Databricks-ADF-Analytics/
│
├── Databricks_notebook/
│   ├── 01_Bronze_rawdata.py        # Event Hub → Delta Lake (streaming)
│   ├── 02_Silver_transformation.py # Cleaning, schema enforcement
│   └── 03_Gold_transform.py        # Star schema, SCD2, metrics
│
├── Docs/
│   ├── Patient_flow_simulated.py   # Simulator (placeholder — safe for GitHub)
│   └── Project_requirements.md
│
├── Notes/                          # Daily implementation notes
│
└── README.md

## Key Implementation Details
Bronze Layer
Reads from Event Hub using Spark's native Kafka connector
AMQP-over-WebSocket transport to handle corporate firewall restrictions on port 5671
Casts binary Kafka payload → JSON string
Writes continuously to Delta Lake via Spark Structured Streaming
Silver Layer
Parses JSON into strongly-typed schema using from_json() + StructType
Cleans intentional dirty data injected by simulator:
Invalid ages (>100) → replaced with randomized valid age
Future admission timestamps → replaced with current_timestamp()
Defensive schema evolution loop handles upstream schema drift
Gold Layer
dim_patient — SCD Type 2 using SHA-256 hash-based change detection + DeltaTable.merge(). Tracks effective_from, effective_to, is_current
dim_department — Simple full-refresh (no SCD2 needed for static reference data)
fact_admissions — Partitioned by admission_date, includes computed metrics (length_of_stay_hours, is_currently_admitted)
ADF Orchestration
Get Metadata activity checks silver container for new files
If Condition: @greaterOrEquals(length(activity('Get Metadata1').output.childItems), 5)
True branch triggers gold Databricks notebook
5-minute schedule trigger for continuous operation

## Real-World Challenges Solved
Challenge	Root Cause	Solution
Event Hub connection failures	Corporate firewall blocking AMQP port 5671	Switched to TransportType.AmqpOverWebsocket (port 443)
kafka-python incompatible	Python 3.14 not supported by library	Switched to azure-eventhub SDK with Spark's native Kafka connector
Databricks cluster wouldn't start	Trial DBU allocation expired independently of Azure subscription credit	Created new Hybrid-type workspace under Pay-As-You-Go subscription
spark.conf.set() fails on Serverless	Serverless compute restricts Hadoop-level config	Switched to all-purpose cluster; documented limitation
Cluster creation quota error	Standard DDSv5 Family vCPU quota = 0 after subscription upgrade	Submitted quota increase via Azure Portal → Quotas → My Quotas
ADF notebook activity failing	Notebook path required /Workspace/ prefix, no .py extension	Corrected path format in ADF Notebook activity

## How to Run

1. Clone the repo

bash
git clone https://github.com/Nived-P/Medical-Patient-Dataflow-Databricks-ADF-Analytics.git

2. Set up Azure resources

Azure Event Hub (Standard tier)
Azure Databricks (Premium, Hybrid type)
ADLS Gen2 with containers: bronze, silver, gold
Azure Data Factory
Azure Key Vault

3. Store secrets in Key Vault

Event Hub connection string
Storage Account access key

4. Create Databricks secret scope linked to Key Vault

https://<your-workspace-url>#secrets/createScope

5. Run the simulator

bash
pip install azure-eventhub websocket-client
python Docs/Patient_flow_simulated_local.py

6. Run notebooks in order in Databricks

01_Bronze_rawdata.py → 02_Silver_transformation.py → 03_Gold_transform.py

7. Deploy ADF pipeline

Get Metadata → If Condition → Notebook activity (gold)
Certification
Databricks Certified Associate Developer for Apache Spark
Author

Nived P
Data Engineer | Databricks Certified | Azure Data Engineering

GitHub · LinkedIn:https://www.linkedin.com/in/nived-p-59a480213/