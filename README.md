# Data Pipeline for NYC 311 data

## Goal

Create a an automated ETL pipeline to prepare NYC 311 data for analysis.

Note: This is built as the Capstone Project for Udacity's Data Engineering Nanodegree.

### Problem

As a transplant into New York City, noise is one thing I expected to hear a lot. But, not everyone seems to handle it well, including my downstairs neighbor who comes knocking after every step. I wanted to take a look into what blocks complain the most, about noise and otherwise. In addition, I wanted to explore weather as another dimension that could affect the type of complaints recieved (ex. if it's cold there could be an increase in 311 service requests for heating).

### Solution

In order to effectively gain insight from NYC 311 data, a data engineer needs to structure the data and load it into a database. The proposed plan consists of a Python ETL pipeline with two stages:

- Stage 1a: Extract raw 311 data from API
  - Query NYC Open Data 311 Endpoint
  - Save JSON data in S3
- Stage 1b: Extract raw weather data from API
  - Query DarkSky Endpoint
  - Save CSV data in S3
- Stage 2: Transform raw data into star schema for analytics
  - Extract each data file hosted on S3.
  - Load data into staging tables on Redshift.
  - Transform and load data into analytics tables with star schema on Redshift.
  - Perform data quality checks to ensure reliable data.
- Stage 3: Perform analysis
  - Use

![Alt text](nyc_311_ERD.png?raw=true "NYC 311 ERD")


## Data

### 311 Complaint Dataset

- This dataset is a subset of real NYC 311 data from the City of New York.
- Files live on S3 with the link ???
- Each file is in JSON format and contains data about the 311 complaint.
  - The files are partitioned by year and month of each complaint.
  - 311_complaints/{year}/{month}/{year}-{month}-{day}.json

### Weather Dataset

- This dataset is an hourly temperature recording powered by DarkSky.
- File lives on S3 with the link ???
- File is in CSV format and contains data
  - The files are partitioned by year, month, and day.
  - temperature/{year}/{month}/{day}/{year}-{month}-{day}.csv


## Data Models

### Entities

The database is structured as a star schema for analysis of complaints. As such, the fact table (ie center of the star) will be complaints, and it will have it's associated dimensions related as foreign keys.

Fact table
- complaints: ???

Dimension tables
- ???

### Entity Relationship Diagram (ERD)

![Alt text]()


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
- ???

**Steps to run get_nyc_311_data_dag**
1. Set up Socrata App Token
2. $ airflow webserver
3. $ airflow scheduler
4. Configure default AWS connection with your credentials through local file ~/.aws/credentials or Airflow UI
5. In Airflow UI, create S3 connection
6. Turn on and Trigger DAG in Airflow UI


### get_nyc_weather_data_dag
- ???

**Steps to run get_nyc_weather_data_dag**
1. Set up DarkSky App Token
2. $ airflow webserver
3. $ airflow scheduler
4. Configure default AWS connection with your credentials through local file ~/.aws/credentials or Airflow UI
5. In Airflow UI, create S3 connection
6. Turn on and Trigger DAG in Airflow UI


### load_nyc_311_data_dag
- ??

**Steps to run load_nyc_311_data_dag**
1. Start up Redshift cluster
2. $ airflow webserver
3. $ airflow scheduler
4. Configure default AWS connection with your credentials through local file ~/.aws/credentials or Airflow UI
5. In Airflow UI, create Redshift cluster connection
6. Turn on and Trigger DAG in Airflow UI


## Future Growth Scenarios

A description of how I would approach the problem differently under the following scenarios:
- If the data was increased by 100x.
  - ???
- If the pipelines were run on a daily basis by 7am.
  - Launch a dedicated EC2 server that contained Airflow so it could guarantee that the DAGs ran every day.
  - Set up a dedicated metadb and s3 bucket for airflow logging to ensure logs persist and can be viewed across multiple machines
  - ???
- If the database needed to be accessed by 100+ people.
  - Use Apache Superset to create a more user friendly way to analyze the data.
  - ???
