# Azure Synapse (data eng/data analytics part??)
- business ready data in gold is to be pulled into Azure synapse SQL pool for warehousing.Power BI is connected here for dashboard creation.
- Create Synapse analytics workspace from azure and connect with created synpase container in stoarge account.Then open the synapse studio.
- Create the SQL pool(warehouse) from synapse studio.
- create a new SQL script from data---SQL pool(SQL db)
- create master key in script and also create scope for connecting with storage account.
- Define the data source(the gold container).
- Create external file format of type parquet
- Create external tables for all 3 gold tables, and data is refered from storage account gold container. eg:dim_patient,dim_department,fact_patient_flow.
- using select query, verify all the data reached the external tables.
## PowerBI connection with SQL Pool(data analytics part)
- select data source here as data analtics SQL.
