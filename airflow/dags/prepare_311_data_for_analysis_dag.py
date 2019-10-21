from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import (StageToRedshiftOperator, LoadFactOperator,
                                LoadDimensionOperator, DataQualityOperator,
                                CreateTableInRedshiftOperator)
from helpers import SqlQueries


default_args = {
    'owner': 'wyatt',
    'depends_on_past': False,
    'start_date': datetime(2019, 10, 15),
    'email_on_failure': False,
    'retries': 0
}

dag = DAG('prepare_311_data_for_analysis_dag',
          default_args=default_args,
          description='Load and transform NYC 311 and weather data in Redshift',
          schedule_interval='0 4 * * *',
          catchup=False
        )

start_operator = DummyOperator(
    task_id='Begin_execution',
    dag=dag
)

# create_staging_service_request_table = CreateTableInRedshiftOperator(
#     task_id='Create_staging_service_request_table_in_redshift',
#     dag=dag,
#     redshift_conn_id="redshift",
#     sql_drop = SqlQueries.staging_service_request_table_drop,
#     sql_create = SqlQueries.staging_service_request_table_create
# )
#
# create_staging_weather_table = CreateTableInRedshiftOperator(
#     task_id='Create_staging_weather_table_in_redshift',
#     dag=dag,
#     redshift_conn_id="redshift",
#     sql_drop = SqlQueries.staging_weather_table_drop,
#     sql_create = SqlQueries.staging_weather_table_create
# )
#
# stage_service_request_to_redshift = StageToRedshiftOperator(
#     task_id='Stage_service_request_from_s3_to_redshift',
#     dag=dag,
#     redshift_conn_id="redshift",
#     aws_credentials_id="aws_credentials",
#     s3_path="s3://nyc-311-data-us-east-2",
#     redshift_target_table = "staging_service_request",
#     redshift_aws_region = "us-east-2",
#     s3_file_type="json"
# )
#
# stage_weather_to_redshift = StageToRedshiftOperator(
#     task_id='Stage_weather_from_s3_to_redshift',
#     dag=dag,
#     redshift_conn_id="redshift",
#     aws_credentials_id="aws_credentials",
#     s3_path="s3://nyc-weather-data-us-east-2",
#     redshift_target_table = "staging_weather",
#     redshift_aws_region = "us-east-2",
#     s3_file_type="csv"
# )

create_weather_table = CreateTableInRedshiftOperator(
    task_id='Create_weather_table_in_redshift',
    dag=dag,
    redshift_conn_id="redshift",
    sql_drop = SqlQueries.weather_table_drop,
    sql_create = SqlQueries.weather_table_create
)

load_weather_table = LoadDimensionOperator(
    task_id='Load_weather_dim_table',
    dag=dag,
    redshift_conn_id="redshift",
    sql_select=SqlQueries.weather_table_insert,
    dimension_table="weather"
)

create_location_table = CreateTableInRedshiftOperator(
    task_id='Create_location_table_in_redshift',
    dag=dag,
    redshift_conn_id="redshift",
    sql_drop = SqlQueries.location_table_drop,
    sql_create = SqlQueries.location_table_create
)

load_location_table = LoadDimensionOperator(
    task_id='Load_location_dim_table',
    dag=dag,
    redshift_conn_id="redshift",
    sql_select=SqlQueries.location_table_insert,
    dimension_table="location"
)

create_complaint_type_table = CreateTableInRedshiftOperator(
    task_id='Create_complaint_type_table_in_redshift',
    dag=dag,
    redshift_conn_id="redshift",
    sql_drop = SqlQueries.complaint_type_table_drop,
    sql_create = SqlQueries.complaint_type_table_create
)

load_complaint_type_table = LoadDimensionOperator(
    task_id='Load_complaint_type_dim_table',
    dag=dag,
    redshift_conn_id="redshift",
    sql_select=SqlQueries.complaint_type_table_insert,
    dimension_table="complaint_type",
    specified_fields="complaint_type, descriptor"
)

create_agency_table = CreateTableInRedshiftOperator(
    task_id='Create_agency_table_in_redshift',
    dag=dag,
    redshift_conn_id="redshift",
    sql_drop = SqlQueries.agency_table_drop,
    sql_create = SqlQueries.agency_table_create
)

load_agency_table = LoadDimensionOperator(
    task_id='Load_agency_dim_table',
    dag=dag,
    redshift_conn_id="redshift",
    sql_select=SqlQueries.agency_table_insert,
    dimension_table="agency",
    specified_fields="agency_acronym, agency_name"
)

create_submission_type_table = CreateTableInRedshiftOperator(
    task_id='Create_submission_type_table_in_redshift',
    dag=dag,
    redshift_conn_id="redshift",
    sql_drop = SqlQueries.submission_type_table_drop,
    sql_create = SqlQueries.submission_type_table_create
)

load_submission_type_table = LoadDimensionOperator(
    task_id='Load_submission_type_dim_table',
    dag=dag,
    redshift_conn_id="redshift",
    sql_select=SqlQueries.submission_type_table_insert,
    dimension_table="submission_type",
    specified_fields="submission_type"
)

create_status_table = CreateTableInRedshiftOperator(
    task_id='Create_status_table_in_redshift',
    dag=dag,
    redshift_conn_id="redshift",
    sql_drop = SqlQueries.status_table_drop,
    sql_create = SqlQueries.status_table_create
)

load_status_table = LoadDimensionOperator(
    task_id='Load_status_dim_table',
    dag=dag,
    redshift_conn_id="redshift",
    sql_select=SqlQueries.status_table_insert,
    dimension_table="status",
    specified_fields="status"
)

create_service_request_table = CreateTableInRedshiftOperator(
    task_id='Create_service_request_table_in_redshift',
    dag=dag,
    redshift_conn_id="redshift",
    sql_drop = SqlQueries.service_request_table_drop,
    sql_create = SqlQueries.service_request_table_create
)

load_service_request_table = LoadFactOperator(
    task_id='Load_service_request_fact_table',
    dag=dag,
    redshift_conn_id="redshift",
    sql_select=SqlQueries.service_request_table_insert,
    fact_table="service_request"
)

# check_time_table = DataQualityOperator(
#     task_id='Check_time_table',
#     dag=dag,
#     redshift_conn_id="redshift",
#     table="time"
# )

end_operator = DummyOperator(
    task_id='Stop_execution',
    dag=dag
)

# start_operator >> [create_staging_service_request_table, create_staging_weather_table]
# create_staging_service_request_table >> stage_service_request_to_redshift
# create_staging_weather_table >> stage_weather_to_redshift
# [stage_service_request_to_redshift, stage_weather_to_redshift] >> create_service_request_table
#

start_operator >> [create_weather_table, create_location_table, create_complaint_type_table, create_agency_table, create_submission_type_table, create_status_table]
[create_weather_table, create_location_table, create_complaint_type_table, create_agency_table, create_submission_type_table, create_status_table] >> load_weather_table
[create_weather_table, create_location_table, create_complaint_type_table, create_agency_table, create_submission_type_table, create_status_table] >> load_location_table
[create_weather_table, create_location_table, create_complaint_type_table, create_agency_table, create_submission_type_table, create_status_table] >> load_complaint_type_table
[create_weather_table, create_location_table, create_complaint_type_table, create_agency_table, create_submission_type_table, create_status_table] >> load_agency_table
[create_weather_table, create_location_table, create_complaint_type_table, create_agency_table, create_submission_type_table, create_status_table] >> load_submission_type_table
[create_weather_table, create_location_table, create_complaint_type_table, create_agency_table, create_submission_type_table, create_status_table] >> load_status_table
[load_weather_table, load_location_table, load_complaint_type_table, load_agency_table, load_submission_type_table, load_status_table] >> create_service_request_table
create_service_request_table >> load_service_request_table
load_service_request_table >> end_operator
