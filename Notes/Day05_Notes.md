## Python simulation script:
- Ran the  script  and initially thought like 9093 port doesnt suppport in office wifi.But, same issue happened for hotspot also.
- Then cross verified all the ctredentials in loacl.py file and azure again, but now the error suggests that the azure event hub basic tier doesnt support kafka protocol,so planning to edit that to standard tier.
- Checked the network connection using **Test-NetConnection -ComputerName Hospital-ADB-Eventhub-ns.servicebus.windows.net -Port 9093**, So verified that the issue is not network related.
## Rewriting the simulation script:
- This narrows it down to a library/Python compatibility issue, exactly as suspected. The kafka-python library (especially with the newer async-based internals in recent versions) is likely struggling with SSL/SASL handshake specifics against Python 3.14, which is very new.
- Best fix: switch to Azure's official SDK instead
Rather than fighting kafka-python compatibility, let's use azure-eventhub,Microsoft's official Python SDK for Event Hub. It uses AMQP protocol natively (Event Hub's native protocol, not the Kafka-compatibility layer), so it's more reliable and actually the more "proper" way to do this on Azure specifically.
- Installed azure-eventhub using pip install azure-eventhub
- So we are using AMQP protocol instead of kafka protocol.
- Editing script accordingly.
- Python 3.14 doesnt support SSL handshake using kafka protocol, so we are using azure event hubs own AMQP protocol.(using azure-eventhub, Microsoft's own official library, built specifically for Event Hub's native AMQP protocol.)
-  The above one also hit error:
just add TransportType to your import line, and add the transport_type=TransportType.AmqpOverWebsocket parameter to your producer setup, it is needed for establsihing connection in corporate network
- pip install websocket-client after installing this data got generated, one per second
sample data:Sent to Event Hub: {'patient_id': '8de3ac91-6555-4517-addf-17afbf2d7b72', 'gender': 'Female', 'age': 66, 'department': 'Pediatrics', 'admission_time': '2026-07-27T05:16:11.537558', 'discharge_time': '2026-07-28T05:16:11.537558', 'bed_id': 38, 'hospital_id': 4}
- used ctrl+C to stop the execution as of now.
# challenges faced while running python script for uploading streaming data:
While setting up the real-time ingestion script for Azure Event Hub, the initial approach using the kafka-python library (connecting via Event Hub's Kafka-compatibility layer) consistently failed with connection timeouts, despite verified network reachability (confirmed via Test-NetConnection) and correct credentials. Root cause analysis revealed two layered issues: first, the Event Hub Namespace was on Basic tier, which doesn't support the Kafka protocol at all (requires Standard tier or above); after upgrading to Standard, the kafka-python library still failed due to a likely compatibility issue with Python 3.14 (a very new release, mandated by corporate IT policy). The fix was switching to Microsoft's official azure-eventhub SDK, which uses Event Hub's native AMQP protocol instead of the Kafka-compatibility layer — a more reliable, Microsoft-maintained approach. Even after switching, the AMQP connection was forcibly reset (WinError 10054), pointing to a corporate firewall blocking AMQP's default port (5671); this was resolved by using TransportType.AmqpOverWebsocket, which routes the same AMQP traffic over port 443 (standard HTTPS), and installing the required websocket-client dependency. This troubleshooting reinforced the importance of protocol/transport-layer awareness when working in restrictive corporate network environments.

## Analysing eventhub about the ingested data:
- Able to see 138 event messages generated in 138 seconds.
- to see data : go to event hub--data explorer-- view events.
## Setting up storage account:
- Created a storage account and added 4 containers inside it(bronze,silver,gold and synpaseworkspace).

