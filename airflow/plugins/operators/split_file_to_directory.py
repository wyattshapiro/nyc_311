from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
import os
import json

class SplitFileToDirectoryOperator(BaseOperator):

    @apply_defaults
    def __init__(self,
                 json_input_filepath,
                 output_directory,
                 json_output_filepath,
                 *args, **kwargs):

        super(SplitFileToDirectoryOperator, self).__init__(*args, **kwargs)

        # Map params
        self.json_input_filepath = json_input_filepath
        self.output_directory = output_directory
        self.json_output_filepath = json_output_filepath

    def execute(self, context):
        # read in json
        self.log.info('Reading input file')
        rendered_json_input_filepath = self.json_input_filepath.format(**context)
        json_input = json.loads(open(rendered_json_input_filepath).read())

        # make directory
        self.log.info('Creating directory to store files')
        rendered_output_directory = self.output_directory.format(**context)
        if not os.path.exists(rendered_output_directory):
            os.mkdir(rendered_output_directory)

        # split up file into multiple files under directory
        self.log.info('Writing files')
        for result in json_input:
            # write JSON to file
            rendered_json_output_filepath = rendered_output_directory + self.json_output_filepath.format(unique_id=result['unique_key'])
            with open(rendered_json_output_filepath, 'w') as outfile:
                json.dump(result, outfile)
        self.log.info('Wrote {} json files to {}'.format(len(json_input), rendered_output_directory))
