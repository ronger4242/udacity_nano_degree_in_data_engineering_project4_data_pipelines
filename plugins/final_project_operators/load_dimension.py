from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self,
                redshift_conn_id = "",
                sql_query = "",
                table = "",
                truncate = False,
                *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        # Map params here
        # Example:
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.sql_query = sql_query
        self.truncate = truncate

    def execute(self, context):
        redshift_hook = PostgresHook(self.redshift_conn_id)
        if self.truncate == True:
            self.log.info("Truncating dimension table...")
            redshift_hook.run(f"TRUNCATE TABLE {self.table}")
        self.log.info("Inserting data to dimension table")
        redshift_hook.run("INSERT INTO {} {}".format(self.table, self.sql_query))
