#Healthcare project:

##Setting up:

-Installed VS code from Software centre.
-Git installation from Software centre is in progress.
Issues in downloading python extensions.Working on it

##Brief idea about project/the flow:

-It is basically a real time end-to-end project related to healthcare to analyse the dataflow of patients in a hospital.
-We use Azure event hubs and kafka for real time streaming.
-The Data is ingested to Databricks and transformed using Pyspark:

-Learn about the medallion architecture.
-Schema evolution in delta lake.
-SCD type 2 handling in gold layer.
-Building star schema.

-Data after transformation is loaded into Azure Synapse SQL pool.
-Analytics team uses Power BI for visualization purpose.



