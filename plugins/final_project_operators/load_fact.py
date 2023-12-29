from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadFactOperator(BaseOperator):

    ui_color = '#F98866'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id = "",
                 table = "",
                 sql_query = "",
                 *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        # Map params here
        # Example:
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.sql_query = sql_query


    def execute(self, context):
        redshift_hook = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        self.log.info("Load data from statging to fact table")
        redshift_hook.run("INSERT INTO {} {}".format(self.table, self.sql_query))
