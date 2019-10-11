# Data Pipeline for NYC 311 data

## Goal

Create a an automated ETL pipeline to prepare  NYC 311 data for analysis.

Note: This is built as the Capstone Project for Udacity's Data Engineering Nanodegree.

### Problem

As a transplant into New York City, noise is one thing I expected to hear a lot. But, not everyone seems to handle it well, including my downstairs neighbor who comes knocking after every step. I wanted to take a look into what neighborhoods complain the most, about noise and otherwise.


### Solution

In order to effectively gain insight from NYC 311 data, a data engineer needs to structure the data and load it into a database. The proposed plan consists of a Python ETL pipeline that will:

- Extract each data file hosted on S3.
- Load data into staging tables on Redshift.
- Transform and load data into analytics tables with star schema on Redshift.
- Perform data quality checks.

![Alt text]()

## Data

### 311 Complaint Dataset

- This dataset is a subset of real NYC 311 data from the City of New York.
- Files live on S3 with the link ???
- Each file is in JSON format and contains metadata about the 311 complaint.
  - The files are partitioned by year, month, and day of each complaint.
  - 311_complaints/{year}/{month}/{day}/{complaint_id}.json

### Borough Block Lot (BBL) Dataset

- This dataset is a mapping between Borough Block Lot (BBL) and neighborhood.
- File lives on S3 with the link ???
- File is in CSV format and contains a mapping from BBL to neighborhood.


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

**Steps to run**

1. Navigate to top of project directory
2. Create virtualenv (see Dependencies)
3. Activate virtualenv (see Dependencies)
4. Install requirements (see Dependencies)
5. Start up Redshift cluster
6. $ airflow webserver
7. $ airflow scheduler
8. Configure Airflow connections to AWS and Redshift cluster
9. Turn on and Trigger DAG in Airflow UI
