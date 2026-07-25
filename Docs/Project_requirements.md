## Subject
- Development of Data platform for the  Analytics of real time patient flow and bed occupacy.
## Business background
- Country Health alliance (CHA) is a Hospital group managing nearly 10 Hospitals in North-Central US.
- CHA is now facing challenge in managing realtime patient inflow, their bed occupancy,patient incoming and discharge pattern in every department.
- So requires a Real time data platform which manages the above without any fault.
## Business objectives
- Monitor patient admissions to reduce waiting time.
- Identify the department level bottlenecks/loads (emergency,ICU,surgery)
- Gender based and age based KPI's for demographic insigts.
- Automatic alerts in case of pipeline failures.
## Functional requirements
## 1.Data Source
- Real time patient admission and discharge data from hospital registry.
- Daily batch extracts from Electronic Health Records.
- Department metadata(Staffs,capacity).
## 2.Data Processing and storage
- Store data in medallion architecture (Bronze--Silver--Gold)
- Handle schema evolution when new patient attributes are added.
- Store tables in star schema.
- Implement SCD type2 in patient and department history.
## 3.Analytics
- Use Azure Synapse analytics SQL pool as data warehouse for the storing purpose.
- Build dashboards using power BI
## 4.Orchestration and Automation
- Use Azure Data Factory for the automation of daily batch from the EHR.
- ADF also used to orchestrate real time processing triggers.
- Gold layer refershes for Dashboards.
## 5.Data Quality
- Address the dirty data like duplicate patient id, wrong timestamps,wrong admission time in the silver layer.
## 6.Security and Complaince
- Role based access controls to data based on the departments.
## Deliverables
- Fully functional Azure based data pipelines.
- Power BI Dashboard connected live synapse queries.
- Data Quality and validatiuon reports.
- Full project Documentation
## Success criteria
- Dashboards often refresh for real-time views.
- All pipelines fully automated via adf.
- Schema changes don't cause down time.

