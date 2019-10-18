from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class CreateTableInRedshiftOperator(BaseOperator):

    @apply_defaults
    def __init__(self,
                 redshift_conn_id,
                 sql_drop,
                 sql_create,
                 *args, **kwargs):

        super(CreateTableInRedshiftOperator, self).__init__(*args, **kwargs)

        # Map params
        self.redshift_conn_id = redshift_conn_id
        self.sql_drop = sql_drop
        self.sql_create = sql_create


    def execute(self, context):
        self.log.info("Retrieving credentials")
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        self.log.info("Dropping table in Redshift")
        redshift.run(self.sql_drop)

        self.log.info("Creating table in Redshift")
        redshift.run(self.sql_create)
