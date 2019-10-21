from datetime import datetime
import configparser
from airflow import DAG
from airflow.operators import (QuerySocrataOperator, SplitFileToDirectoryOperator, SaveDirectoryToS3Operator)

config = configparser.ConfigParser()
config.read('nyc_311.cfg')

default_args = {
    'owner': 'wyatt',
    'depends_on_past': False,
    'start_date': datetime(2019, 10, 15),
    'email_on_failure': False,
    'retries': 0
}

dag = DAG('get_nyc_311_data_dag',
          default_args=default_args,
          description='Get 311 data from NYC Open Data and load to S3',
          schedule_interval='0 3 * * *',
          catchup=True,
          max_active_runs=1
        )

query_nyc_311_data = QuerySocrataOperator(
    task_id='Query_nyc_open_data',
    dag=dag,
    provide_context=True,
    socrata_domain='data.cityofnewyork.us',
    socrata_dataset_identifier='fhrw-4uyv',
    socrata_token=config['SOCRATA']['API_TOKEN'],
    json_output_filepath='nyc_311_{yesterday_ds}.json',
    socrata_query_filters={
                            'where': "closed_date between '{yesterday_ds}' and '{ds}'",
                            'limit': 1000000
                           }
)

split_nyc_311_json = SplitFileToDirectoryOperator(
    task_id='Split_nyc_311_json_data',
    dag=dag,
    provide_context=True,
    json_input_filepath='nyc_311_{yesterday_ds}.json',
    output_directory='nyc_311_{yesterday_ds}/',
    json_output_filepath='{unique_id}.json'
)

save_nyc_open_data_to_S3 = SaveDirectoryToS3Operator(
    task_id='Save_nyc_open_data_to_S3',
    dag=dag,
    provide_context=True,
    s3_conn_id='s3',
    s3_bucket='nyc-311-data-us-east-2',
    s3_directory='{execution_date.year}/{execution_date.month}/{execution_date.day}/',
    local_directory='nyc_311_{yesterday_ds}/',
    replace=True
)

query_nyc_311_data >> split_nyc_311_json
split_nyc_311_json >> save_nyc_open_data_to_S3
