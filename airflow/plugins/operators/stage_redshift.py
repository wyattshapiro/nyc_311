from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'

    copy_sql = """COPY {}
                  FROM '{}'
                  ACCESS_KEY_ID '{}'
                  SECRET_ACCESS_KEY '{}'
                  region 'us-west-2'
                  format as json '{}';"""

    @apply_defaults
    def __init__(self,
                 redshift_conn_id,
                 aws_credentials_id,
                 s3_path_json,
                 redshift_target_table,
                 s3_path_schema="auto",
                 *args, **kwargs):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)

        # Map params
        self.redshift_conn_id = redshift_conn_id
        self.aws_credentials_id = aws_credentials_id
        self.s3_path_json = s3_path_json
        self.s3_path_schema = s3_path_schema
        self.redshift_target_table = redshift_target_table


    def execute(self, context):
        self.log.info("Retrieving credentials")
        aws_hook = AwsHook(self.aws_credentials_id)
        credentials = aws_hook.get_credentials()
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        self.log.info("Copying data from S3 to Redshift staging table")
        formatted_sql = StageToRedshiftOperator.copy_sql.format(
            self.redshift_target_table,
            self.s3_path_json,
            credentials.access_key,
            credentials.secret_key,
            self.s3_path_schema
        )
        redshift.run(formatted_sql)
