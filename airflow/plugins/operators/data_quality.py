from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id,
                 table,
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)

        # Map params
        self.redshift_conn_id = redshift_conn_id
        self.table = table

    def execute(self, context):
        self.log.info("Retrieving credentials")
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        self.log.info("Getting record count from table")
        sql_get_record_count = "SELECT COUNT(*) FROM {}".format(self.table)
        records = redshift.get_records(sql_get_record_count)

        self.log.info("Checking SQL response")
        if len(records) < 1 or len(records[0]) < 1:
            raise ValueError("Data quality check failed. %s returned no results", self.table)

        self.log.info("Checking record count")
        num_records = records[0][0]
        if num_records < 1:
            raise ValueError("Data quality check failed. %s contained 0 rows", self.table)

        self.log.info("Data quality on table %s check passed with %s records", self.table, num_records)
