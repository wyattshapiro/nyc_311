# Data Pipeline for NYC 311 data

## Goal

Create an automated ETL pipeline to prepare data for analysis of noise complaints and other 311 service requests in NYC.

### Problem

The City of New York is responsible for the governance of millions of people. They offer a variety of different municipal services that must be managed to take care of streets, buildings, and the people. In order to better understand what services their constituents are using throughout the year, they want to explore the 311 service requests they have received. They are especially interested in how they can accommodate their diverse boroughs (Brooklyn, Bronx, Queens, Manhattan, Staten Island). In addition, they want to explore how weather conditions and seasonal differences affect the type of services received (ex. if it's cold there could be an increase in 311 service requests for no heating in building).

### Technologies

Amazon Web Services is a natural choice to develop as it is a leading cloud provider with a wide array of services. There are three main components in this pipeline.

AWS S3 as the Data Lake
- Object storage service that can store highly unstructured data in many formats
- Used to store a high volume of incoming data
- Highly available and durable against data system failures as it is automatically copied across multiple systems

AWS Redshift as the Data Warehouse
- Online analytical processing (OLAP) that supports analytical processes
- Easy to access and query
- Direct connection to S3 (no additional middleware needed to read/write data)

Apache Airflow as the ETL orchestrator
- Task scheduler for batch operations
- Highly configurable Directed Acyclic Graphs
- Integrates with S3 and Redshift to ensure tasks are scheduled and completed on a regular basis

### ETL Pipelines

In order to effectively gain insight into Noise Complaints and other non-emergency service requests in NYC, I turned to NYC Open Data 311. I needed to extract the data from APIs, store it in a data lake (S3), and transform/load it into a data warehouse (Redshift) with star schema for later analysis.

The proposed plan consists of Python ETL pipelines with the following stages:

- Stage 1a: Extract NYC 311 service request data
  - Query NYC Open Data 311 API Endpoint daily
  - Save JSON data to S3

![Alt text](dag_get_nyc_311_data.png?raw=true "DAG Get NYC 311 data")

- Stage 1b: Extract NYC weather data
  - Query DarkSky API Endpoint daily
  - Save CSV data to S3

![Alt text](dag_get_nyc_weather_data.png?raw=true "DAG Get NYC weather data")

- Stage 2: Transform raw data into star schema for analytics
  - Extract each data file hosted on S3.
  - Load data into staging tables on Redshift.
  - Transform and load data into analytics tables with star schema on Redshift.
  - Perform data quality checks to ensure reliable data.

![Alt text](dag_prepare_311_data_for_analysis.png?raw=true "DAG Prepare data for analysis")


## Data

### 311 Service Request Dataset

- This dataset is a subset of real NYC 311 data from the City of New York.
  - 311 Service Requests are non-emergency requests to municipal services.
- Files live on S3 with the link s3://nyc-311-data-us-east-2
- Each file is in JSON format and contains data about 311 service requests for one day.
  - The files are partitioned by year, month, and day.
  - {year}/{month}/{day}/{id}.json

See https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9 for more information on data.

### Weather Dataset

- This dataset is an hourly temperature measurements powered by DarkSky.
- File lives on S3 with the link s3://nyc-weather-data-us-east-2
- Each file is in CSV format and contains hourly data about NYC temperature for one day.
  - The files are partitioned by year, month, and day.
  - {year}/{month}/nyc_weather_{year}-{month}-{day}.csv

See https://darksky.net/dev/docs for more information on data.


## Data Models

### Entities

The database is structured as a star schema for analysis of 311 service requests. As such, the fact table (ie center of the star) will be service requests, and it will have it's associated dimensions related as foreign keys.

Fact table
- Service Requests: A 311 service request for NYC's non emergency services.

Dimension tables
- Location: Place where service was requested
- Weather: Weather conditions (temp, precipitation) for NYC in one hour.
- Complaint Type: Type of service requested.
- Agency: Agency that service request was sent to.
- Submission Type: How the service was requested (phone, online, etc).
- Status: Current standing of the request (assigned, closed, etc).

See more information in data dictionary, data_dictionary_nyc_311.xlsx

### Entity Relationship Diagram (ERD)

![Alt text](nyc_311_ERD.png?raw=true "NYC 311 ERD")


## Installation

Clone the repo onto your machine with the following command:

$ git checkout https://github.com/wyattshapiro/nyc_311.git


## Dependencies

I use Python 3.7.

See https://www.python.org/downloads/ for information on download.

----

I use virtualenv to manage dependencies, if you have it installed you can run
the following commands from the root code directory to create the environment and
activate it:

$ python3 -m venv venv

$ source venv/bin/activate

See https://virtualenv.pypa.io/en/stable/ for more information.

----

I use pip to install dependencies, which comes installed in a virtualenv.
You can run the following to install dependencies:

$ pip install -r requirements.txt

See https://pip.pypa.io/en/stable/installing/ for more information.

----

I use AWS S3 and Redshift for data storage and processing.

See https://aws.amazon.com/ for more information.

----

I use Apache Airflow to orchestrate and schedule tasks.

There are several main directories for Airflow:

- dags/: contains all DAGs (Directed Acyclic Graph)
- plugins/: contains all customizable code that can be leveraged by DAGs
- logs/: contains all log files that track code execution
See https://airflow.apache.org/ for more information.


## Usage

1. Navigate to top of project directory
2. Create virtualenv (see Dependencies)
3. Activate virtualenv (see Dependencies)
4. Install requirements (see Dependencies)

### get_nyc_311_data_dag
Extracts yesterday's closed NYC 311 service requests and saves to S3.

**Steps to run get_nyc_311_data_dag**
1. Set up Socrata App Token to request NYC 311 data
2. $ airflow webserver
3. $ airflow scheduler
4. Configure default AWS connection with your credentials through local file ~/.aws/credentials or Airflow UI
5. In Airflow UI, create S3 connection
6. Turn on and Trigger DAG in Airflow UI

### get_nyc_weather_data_dag
Extracts yesterday's NYC weather from DarkSky and saves to S3.

**Steps to run get_nyc_weather_data_dag**
1. Set up DarkSky App Token to request NYC weather data
2. $ airflow webserver
3. $ airflow scheduler
4. Configure default AWS connection with your credentials through local file ~/.aws/credentials or Airflow UI
5. In Airflow UI, create S3 connection
6. Turn on and Trigger DAG in Airflow UI

### prepare_311_data_for_analysis_dag
Loads and transforms NYC 311 service requests and weather into star schema in Redshift for analysis.

**Steps to run prepare_311_data_for_analysis_dag**
1. Start up Redshift cluster
2. $ airflow webserver
3. $ airflow scheduler
4. Configure default AWS connection with your credentials through local file ~/.aws/credentials or Airflow UI
5. In Airflow UI, create Redshift cluster connection
6. Turn on and Trigger DAG in Airflow UI


## Future Analysis

Potential questions of interest to the City of New York:

- What are the most popular complaints per Borough for 2019 (Year to Date)?
- What borough has the most noise complaints for 2019 (Year to Date)?
- What service requests are at the highest demand at different temperature ranges for 2019 (Year to Date)?

Sample queries to answer these questions can be found in airflow/plugins/helpers/sql_queries.py

## Future Growth Scenarios

A description of how I would approach the problem differently under the following scenarios:
- If the data was increased by 100x.
  - In order to process billions of rows of data, I could turn to computing on Spark. Spark is an open source distributed cluster-computing framework. Because I chose to use S3 as a Data Lake, I could seamlessly integrate Spark with my current cloud environment using AWS Elastic Map Reduce (EMR) to manage the nodes.
  - Also, I could switch the "Prepare data for analysis" DAG to append new rows to the tables instead of resetting the tables on every run. This way I only have to process 311 and weather data from a short time period instead of all of it.

- If the pipelines were run on a daily basis by 7am.
  - Launch a dedicated AWS EC2 server that contained Airflow.
  - Set up a dedicated metadb and s3 bucket for Airflow logging to ensure logs persist even after resetting the database.
  - Configure email alerts on failure, so that if a problem occurs a teammate or I could be notified quickly.
  - Add a Service Level Agreement to Airflow to make sure the data was prepared for the end users on an agreed upon schedule. This would help indicate if there were performance issues or if we needed to scale up the Airflow instance.

- If the database needed to be accessed by 100+ people.
  - If there are many users that need to access the database, I would want to optimize the most common queries running against Redshift. One way to do this is to specify sort_keys for these common queries, where each table's sort key would act like an index. This would result in query filters scanning data more efficiently.
  - I could also change the distribution style on the Redshift nodes to accommodate JOIN heavy queries. If the dimension tables are small enough they should be broadcast to all nodes, as this makes JOINs more efficient since they don't need to traverse nodes to find the necessary data.
  - For short running queries, I could turn to enabling short query acceleration (SQA) which would allow shorter queries to run ahead of those that take a long time. This way results are delivered more quickly to users.
  - Also, for non technical users, I could connect an instance of Apache Superset to create a more user friendly way to analyze the data. This open source dashboard tool could be connected to Redshift and pre-programmed with relevant graphs to the end users. This could be especially helpful to create reusable dashboards for c-suite execs, managers, etc.
