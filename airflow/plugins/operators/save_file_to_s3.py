from airflow.hooks.S3_hook import S3Hook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class SaveFileToS3Operator(BaseOperator):

    @apply_defaults
    def __init__(self,
                 s3_conn_id,
                 s3_bucket,
                 s3_key,
                 local_filepath,
                 replace=False,
                 *args, **kwargs):

        super(SaveFileToS3Operator, self).__init__(*args, **kwargs)

        # Map params
        self.s3_conn_id = s3_conn_id
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.local_filepath = local_filepath
        self.replace = replace

    def execute(self, context):
        self.log.info('Retrieving credentials')
        s3_hook = S3Hook(self.s3_conn_id)

        # render macros to variables
        rendered_local_filepath = self.local_filepath.format(**context)
        rendered_s3_key = self.s3_key.format(**context)
        rendered_s3_bucket = self.s3_bucket.format(**context)

        # save file to S3
        self.log.info('Saving local file to S3')
        s3_hook.load_file(filename=rendered_local_filepath,
                          bucket_name=rendered_s3_bucket,
                          key=rendered_s3_key,
                          replace=self.replace)
        self.log.info('Saved local file {} to bucket {}, key {}'.format(rendered_local_filepath, rendered_s3_bucket, rendered_s3_key))
