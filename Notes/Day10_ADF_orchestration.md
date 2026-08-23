# Azure Data Factory based orchestration (2:12-2:36)
- create data factory, name-Hospital-ADF-nibu.Then launch studio for creation of pipeline.
- Our aim is to run gold databricks notebook.We need to create one more secret(databricks-connection) in existing key vault(Hospital-ADB-vault) for storing the databricks access token.
- For ADF to access the key vault,provided access control (IAM) to keyvault role "key vault secrets user"  and added ADF as member.
## Creation of linked services
- 1.Hospital_vault (connecting keyvault)
- 2.Hospital_Storage (to connect ADLS Gen2)
- 3.Hospital_databricks( to connect databricks)
- give the generated azure keyvault authentication details here.
 
## Creation of dataset(name-Parquet1)
-  Data is taken from the silver path, file format- parquet and provide "Hospital_Storage" as the linked service.
 ## ADF pipeline creation
 ### Activity 1 - Get metadata
 - provide the created Parquet1 dataset here as the source to get data.
 - filed list - child items
 ### Activity 2 - If condition
 - condition - @greaterOrEquals(length(activity('Get Metadata1').output.childItems), 5)
 - If true run notebook of gold
 - Connect Activity 1 and Activity 2 in pipeline in such a way that if silver table has 5 new records, trigger will generated and gold transformation note book will run.
 ## Add a Trigger
 - schedule based trigger which runs every 5 minutes is generated
 - Then validate all created linked service, dataset and activities in pipeline and run debug for an initial check
 - Monitered the queued pipeline run and went succesful.
  ## pipeline failure alert:
  - Azure -- monitor-- alert rule-- select pipeline --- alert on failure to personal mail.