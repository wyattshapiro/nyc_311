from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadFactOperator(BaseOperator):

    ui_color = '#F98866'

    load_sql = """INSERT INTO {}
                  {};"""

    @apply_defaults
    def __init__(self,
                 redshift_conn_id,
                 sql_select,
                 fact_table,
                 *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)

        # Map params
        self.redshift_conn_id = redshift_conn_id
        self.sql_select=sql_select
        self.fact_table=fact_table

    def execute(self, context):
        self.log.info("Retrieving credentials")
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        self.log.info('Loading Fact table')
        formatted_load_sql = LoadFactOperator.load_sql.format(
            self.fact_table,
            self.sql_select)
        redshift.run(formatted_load_sql)
