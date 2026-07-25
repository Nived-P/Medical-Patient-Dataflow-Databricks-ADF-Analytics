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
- import required python modules(random,json,uuid,time)
- event hub or kafka messages are usually sent as json strings.
- Kafkaproducer is the actual client which sents messages to event hub.
- add config names to kafka event hub, namespace and connection strings
- setup the kafka producer,This creates the connection object that will actually send messages
- create fake data pools for departments and gender.
- injecting dirty data ex:-Age>100 and admission time is future time.
- Generate one fake patient record
- Then run this event continously, like one per second.