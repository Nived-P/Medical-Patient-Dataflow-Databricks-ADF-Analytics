# import required python modules(random,json,uuid,time)
#event hub or kafka messages are usually sent as json strings.
# azure event hub is azure official SDK for event hub.
import json
import random
import uuid
import time
from datetime import datetime, timedelta
from azure.eventhub import EventHubProducerClient, EventData

# Event Hub Configuration
CONNECTION_STRING = "<<NAMESPACE_CONNECTION_STRING>>"
EVENT_HUB_NAME = "<<EVENT_HUB_NAME>>"

producer = EventHubProducerClient.from_connection_string(
    conn_str=CONNECTION_STRING,
    eventhub_name=EVENT_HUB_NAME
)

# Departments in hospital
departments = ["Emergency", "Surgery", "ICU", "Pediatrics", "Maternity", "Oncology", "Cardiology"]

# Gender categories
genders = ["Male", "Female"]

# Helper function to introduce dirty data
def inject_dirty_data(record):
    # 5% chance to have invalid age
    if random.random() < 0.05:
        record["age"] = random.randint(101, 150)
    # 5% chance to have future admission timestamp
    if random.random() < 0.05:
        record["admission_time"] = (datetime.utcnow() + timedelta(hours=random.randint(1, 72))).isoformat()
    return record
#Generate one fake patient record
def generate_patient_event():
    admission_time = datetime.utcnow() - timedelta(hours=random.randint(0, 72))
    discharge_time = admission_time + timedelta(hours=random.randint(1, 72))
    event = {
        "patient_id": str(uuid.uuid4()),
        "gender": random.choice(genders),
        "age": random.randint(1, 100),
        "department": random.choice(departments),
        "admission_time": admission_time.isoformat(),
        "discharge_time": discharge_time.isoformat(),
        "bed_id": random.randint(1, 500),
        "hospital_id": random.randint(1, 7)  # Assuming 7 hospitals in network
    }
    return inject_dirty_data(event)
#Run this continously
if __name__ == "__main__":
    try:
        while True:
            event = generate_patient_event()
            event_data_batch = producer.create_batch()
            event_data_batch.add(EventData(json.dumps(event)))
            producer.send_batch(event_data_batch)
            print(f"Sent to Event Hub: {event}")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopped by user.")
    finally:
        producer.close()