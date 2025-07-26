# ETL-Trip-API-Python-Sql
  📌 Project Description
This project automates the extraction, transformation, and loading (ETL) of telematics data from Jaltest’s API into a SQL Server database for further analysis and reporting. It is designed to handle large volumes of vehicle trip data efficiently by incrementally fetching new information and normalizing complex JSON responses.

Key Components and Workflow:

Authentication & API Request Signing:
The scripts use HMAC-SHA1 to generate API request signatures based on a shared secret key. This secure authentication ensures that all API calls are authorized and tamper-proof.

Fetching Vehicle List:
The first step retrieves all vehicles associated with a customer identification number (CIF). The vehicle list includes unique identifiers like number plates, which are used in subsequent API requests.

Incremental Trip Data Retrieval:
To avoid redundant data fetching and reduce API load, the system tracks the last processed trip timestamp in a local file (TripIdJaltest_Agg.txt). Each run fetches trip data only from the last saved timestamp to the current time, making the process incremental and efficient.

Detailed Trip Information Retrieval:
For each trip in the fetched list, detailed telematics data is requested. This includes comprehensive metrics such as:

Braking and acceleration patterns

Fuel consumption and energy use

RPM and speed distributions

Inertia and orography effects

Weight summaries

Driver details and behaviors

Data Normalization and Flattening:
The API returns deeply nested JSON structures. The project uses pandas.json_normalize to flatten these into structured tabular data, renaming nested fields to meaningful column names. It also handles lists of nested records, exploding and expanding them into separate rows or columns as appropriate.

Data Cleaning:
Columns with irrelevant or redundant information are removed to optimize the dataset. Fields containing dictionaries are converted to JSON strings to maintain data integrity during database insertion.

Database Integration:
Using SQLAlchemy with a pyodbc connection, the cleaned and normalized dataset is appended to a Microsoft SQL Server table (TripID_Jaltest_Agg). This integration enables seamless ingestion into enterprise data warehouses and downstream BI tools.

Logging and Error Handling:
The scripts print detailed status updates for API requests, including authorization headers, request URLs, and responses. Errors in fetching data are logged with HTTP status codes and messages, allowing easy troubleshooting.

Time Zone Adjustment:
The project adjusts timestamps by adding one hour to align with the local time zone, ensuring all datetime fields are consistent with business reporting requirements.

 ✅ This ETL pipeline provides a robust and scalable solution for fleet telematics data collection, enabling operational teams to monitor vehicle performance, driver behavior, and trip characteristics with high granularity and reliability.

