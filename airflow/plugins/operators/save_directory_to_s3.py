from airflow.hooks.S3_hook import S3Hook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
import os

class SaveDirectoryToS3Operator(BaseOperator):

    @apply_defaults
    def __init__(self,
                 s3_conn_id,
                 s3_bucket,
                 s3_directory,
                 local_directory,
                 replace=False,
                 *args, **kwargs):

        super(SaveDirectoryToS3Operator, self).__init__(*args, **kwargs)

        # Map params
        self.s3_conn_id = s3_conn_id
        self.s3_bucket = s3_bucket
        self.s3_directory = s3_directory
        self.local_directory = local_directory
        self.replace = replace

    def execute(self, context):
        self.log.info('Retrieving credentials')
        s3_hook = S3Hook(self.s3_conn_id)

        # render macros to variables
        rendered_s3_bucket = self.s3_bucket.format(**context)
        rendered_s3_directory = self.s3_directory.format(**context)
        rendered_local_directory = self.local_directory.format(**context)

        # save file to S3
        self.log.info('Saving local directory to S3')
        local_file_list = os.listdir(rendered_local_directory)
        for local_file in local_file_list:
            rendered_s3_key = rendered_s3_directory + local_file
            rendered_local_file = rendered_local_directory + local_file
            self.log.info(rendered_s3_key)
            s3_hook.load_file(filename=rendered_local_file,
                              bucket_name=rendered_s3_bucket,
                              key=rendered_s3_key,
                              replace=self.replace)
        self.log.info('Saved {} locals file to bucket {}'.format(len(local_file_list), rendered_s3_bucket))
