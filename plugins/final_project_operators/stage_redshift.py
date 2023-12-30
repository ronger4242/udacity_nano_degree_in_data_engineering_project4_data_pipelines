from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.secrets.metastore import MetastoreBackend

class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'

    template_fields = ('s3_key',)

    copy_sql = """
        COPY {}
        FROM '{}'
        ACCESS_KEY_ID '{}'
        SECRET_ACCESS_KEY '{}'
        FORMAT AS json '{}';
    """

    @apply_defaults
    def __init__(self,
                 redshift_conn_id = "",
                 aws_credentials_id = "",
                 table = "",
                 s3_bucket = "",
                 s3_key = "",
                 log_json_file = "",
                 *args, **kwargs):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.aws_credentials_id = aws_credentials_id
        self.table = table
        self.s3_bucket = s3_bucket 
        self.s3_key = s3_key
        self.log_json_file = log_json_file
        #self.execution_date = kwargs.get('execution_date')

    def execute(self, context):
        metastoreBackend = MetastoreBackend()
        aws_connection = metastoreBackend.get_connection(self.aws_credentials_id)
        redshift_hook = PostgresHook(postgres_conn_id = self.redshift_conn_id)

        self.log.info("Deleting data from destination table")
        trucate_sql = "TRUNCATE FROM {}".format(self.table)
        redshift_hook.run(truncate_sql)

        self.log.info("copy data from s3 to redshift")
        s3_key_flex = str(self.s3_key).format(**context)
        s3_path = "s3://{}/{}".format(self.s3_bucket, s3_key_flex)

        # if self.execution_date:
        #     year = self.execution_date.strftime("%Y")
        #     month = self.execution_date.strftim("%m")
        #     s3_path = '/'.join([s3_path,str(year),str(month)])
        
        print('s3_path',s3_path)
        
        if self.log_json_file != "":
            self.log_json_file = "s3://{}/{}".format(self.s3_bucket, self.log_json_file)
            formatted_sql = StageToRedshiftOperator.copy_sql.format(
                self.table,
                s3_path,
                aws_connection.login,
                aws_connection.password,
                self.log_json_file
            )
        else:
            formatted_sql = StageToRedshiftOperator.copy_sql.format(
                self.table,
                s3_path,
                aws_connection.login,
                aws_connection.password,
                "auto"
            )

        redshift_hook.run(formatted_sql)
        self.log.info("Successfully copied data from s3 to redshift table{self.table}")





