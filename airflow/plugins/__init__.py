from __future__ import division, absolute_import, print_function

from airflow.plugins_manager import AirflowPlugin

import operators
import helpers

# Defining the plugin class
class UdacityPlugin(AirflowPlugin):
    name = "udacity_plugin"
    operators = [
        operators.StageToRedshiftOperator,
        operators.LoadFactOperator,
        operators.LoadDimensionOperator,
        operators.DataQualityOperator,
        operators.CreateTableInRedshiftOperator,
        operators.QuerySocrataOperator,
        operators.GetDarkSkyWeatherOperator,
        operators.SaveFileToS3Operator,
        operators.SaveDirectoryToS3Operator,
        operators.SplitFileToDirectoryOperator
    ]
    helpers = [
        helpers.SqlQueries
    ]
