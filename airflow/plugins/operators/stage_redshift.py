from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'

    copy_sql_json = """COPY {}
                  FROM '{}'
                  ACCESS_KEY_ID '{}'
                  SECRET_ACCESS_KEY '{}'
                  region '{}'
                  format as {} '{}';"""

    copy_sql_csv = """COPY {}
                  FROM '{}'
                  ACCESS_KEY_ID '{}'
                  SECRET_ACCESS_KEY '{}'
                  region '{}'
                  format as {}
                  IGNOREHEADER 1;"""

    @apply_defaults
    def __init__(self,
                 redshift_conn_id,
                 aws_credentials_id,
                 s3_path,
                 redshift_target_table,
                 s3_file_type,
                 redshift_aws_region,
                 s3_path_json_schema="auto",
                 *args, **kwargs):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)

        # Map params
        self.redshift_conn_id = redshift_conn_id
        self.aws_credentials_id = aws_credentials_id
        self.s3_path = s3_path
        self.s3_path_json_schema = s3_path_json_schema
        self.s3_file_type = s3_file_type
        self.redshift_aws_region=redshift_aws_region
        self.redshift_target_table = redshift_target_table


    def execute(self, context):
        self.log.info("Retrieving credentials")
        aws_hook = AwsHook(self.aws_credentials_id)
        credentials = aws_hook.get_credentials()
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        self.log.info("Copying data from S3 to Redshift staging table")
        if self.s3_file_type.lower() == 'csv':
            formatted_sql = StageToRedshiftOperator.copy_sql_csv.format(
                self.redshift_target_table,
                self.s3_path,
                credentials.access_key,
                credentials.secret_key,
                self.redshift_aws_region,
                self.s3_file_type
            )
        else:
            formatted_sql = StageToRedshiftOperator.copy_sql_json.format(
                self.redshift_target_table,
                self.s3_path,
                credentials.access_key,
                credentials.secret_key,
                self.redshift_aws_region,
                self.s3_file_type,
                self.s3_path_json_schema
            )

        redshift.run(formatted_sql)
