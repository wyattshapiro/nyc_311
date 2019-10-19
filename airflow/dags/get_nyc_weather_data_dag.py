from datetime import datetime
import configparser
from airflow import DAG
from airflow.operators import (GetDarkSkyWeatherOperator, SaveFileToS3Operator)

config = configparser.ConfigParser()
config.read('nyc_311.cfg')

default_args = {
    'owner': 'wyatt',
    'depends_on_past': False,
    'start_date': datetime(2019, 10, 15),
    'email_on_failure': False,
    'retries': 0
}

dag = DAG('get_weather_data_dag',
          default_args=default_args,
          description='Get hourly NYC weather data for the day from DarkSky and load to S3',
          schedule_interval='0 3 * * *',
          catchup=True,
          max_active_runs=1
          )

get_nyc_weather_data = GetDarkSkyWeatherOperator(
    task_id='Get_nyc_weather_data',
    dag=dag,
    provide_context=True,
    dark_sky_api_token=config['DARKSKY']['API_TOKEN'],
    latitude=config['DARKSKY']['NYC_LATITUDE'],
    longitude=config['DARKSKY']['NYC_LONGITUDE'],
    forecast_date_str='{yesterday_ds}',
    csv_output_filepath='nyc_weather_{yesterday_ds}.csv',
)

save_nyc_weather_data_to_S3 = SaveFileToS3Operator(
    task_id='Save_nyc_weather_data_to_S3',
    dag=dag,
    provide_context=True,
    s3_conn_id='s3',
    s3_bucket='nyc-weather-data-us-east-2',
    s3_key='{execution_date.year}/{execution_date.month}/nyc_weather_{yesterday_ds}.csv',
    local_filepath='nyc_weather_{yesterday_ds}.csv',
    replace=True
)

get_nyc_weather_data >> save_nyc_weather_data_to_S3
