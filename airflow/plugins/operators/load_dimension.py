from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'

    load_sql = """INSERT INTO {}
                  {};"""
    load_sql_specified_fields = """INSERT INTO {} ({})
                                {};"""

    @apply_defaults
    def __init__(self,
                 redshift_conn_id,
                 sql_select,
                 dimension_table,
                 specified_fields=None,
                 append_only=True,
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)

        # Map params
        self.redshift_conn_id = redshift_conn_id
        self.sql_select=sql_select
        self.dimension_table=dimension_table
        self.specified_fields=specified_fields
        self.append_only = append_only

    def execute(self, context):
        self.log.info("Retrieving credentials")
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        if not self.append_only:
            self.log.info('Deleting data in %s Dimension table', self.dimension_table)
            formatted_delete_sql = """DELETE FROM {}""".format(self.dimension_table)
            redshift.run(formatted_delete_sql)

        self.log.info('Loading %s Dimension table', self.dimension_table)
        if self.specified_fields is None:
            formatted_load_sql = LoadDimensionOperator.load_sql.format(
                self.dimension_table,
                self.sql_select)
        else:
            formatted_load_sql = LoadDimensionOperator.load_sql_specified_fields.format(
                self.dimension_table,
                self.specified_fields,
                self.sql_select)
        redshift.run(formatted_load_sql)
