## Architecture
- Azure event hubs with a kafka engine will provide real time source streaming data.
- Raw data from event hub is ingested to data lake bronze layer.
- These data cleansed and ingested into silver layer.
- Transformed business ready data is ingested to gold layer.
- Databricks is used as a platform for all the above mentioend data processing.
- ADF is used for orchestrating pipeline from Silver-gold.
- Data Analytics:- Gold layer-- Azure Synapse SQL pool-- powerBI.
- Secrets in Azure key vault is used for storing connection strings.Azure AD is used to provide access to key vaults.
## Code simulated for source data
