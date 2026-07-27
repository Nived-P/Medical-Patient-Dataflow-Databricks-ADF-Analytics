## Azure setup:
- Login Azure free trail with personal account
- 200 USD available for first 30 days.
- 12 month free for 20+ selected services aka always free tier.
- Azure event hubs is free for first 30 days only.
- Logged into Azure account and created a budget of 150 USD and alert will come to mail once the usage reaches 120 USD.
## Azure event hubs:
- There is already a default azure subscription available.
- We are creating the namespace(container) for the event hub first.
- Created Azure event hub on top of the name space.
- Then edit the below things in Patient_flow_simulated.py after fetching details from the event hub and namespace:

EVENTHUBS_NAMESPACE = "<<NAMESPACE_HOSTNAME>>"
EVENT_HUB_NAME = "<<EVENT_HUB_NAME>>"
CONNECTION_STRING = "<<NAMESPACE_CONNECTION_STRING>>"

- edited the .py file, but to run it python isnt installed in the system yet.So raised access via software centre.(23:00)
- Without wasting time forwarding video and looking up for setup of storage account,databricks account and ADF.
- 