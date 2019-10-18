from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from darksky.api import DarkSky
from darksky.types import languages, units, weather
import datetime
import csv


class GetDarkSkyWeatherOperator(BaseOperator):

    @apply_defaults
    def __init__(self,
                 dark_sky_api_token,
                 latitude,
                 longitude,
                 forecast_date_str,
                 csv_output_filepath,
                 *args, **kwargs):

        super(GetDarkSkyWeatherOperator, self).__init__(*args, **kwargs)

        # Map params
        self.dark_sky_api_token = dark_sky_api_token
        self.latitude = latitude
        self.longitude = longitude
        self.forecast_date_str = forecast_date_str
        self.csv_output_filepath = csv_output_filepath

    def execute(self, context):
        # Authenticate Socrata client
        self.log.info('Authenticate DarkSky client')
        darksky = DarkSky(self.dark_sky_api_token)

        # render macros to for date
        rendered_forecast_date_str = self.forecast_date_str.format(**context)
        forecast_date_obj = datetime.datetime.strptime(rendered_forecast_date_str, '%Y-%m-%d')

        # Get Daily Weather results from API endpoint
        self.log.info('Query API for hourly weather results')
        forecast = darksky.get_time_machine_forecast(
            self.latitude, self.longitude, forecast_date_obj,
            extend=False,  # default `False`
            lang=languages.ENGLISH,  # default `ENGLISH`
            units=units.AUTO,  # default `auto`
            exclude=[weather.CURRENTLY, weather.MINUTELY, weather.DAILY, weather.ALERTS]  # default `[]`
        )
        forecast_hourly_data_object_list = forecast.hourly.data
        forecast_hourly_data_dict_list = []
        for forecast_hourly_data_object in forecast_hourly_data_object_list:
            forecast_hourly_data_dict_list.append(vars(forecast_hourly_data_object))
        self.log.info('Got {} results'.format(len(forecast_hourly_data_dict_list)))

        # Write response to file
        self.log.info('Write response to CSV')
        rendered_csv_output_filepath = self.csv_output_filepath.format(**context)
        keys = forecast_hourly_data_dict_list[0].keys()
        with open(rendered_csv_output_filepath, 'w') as outfile:
            dict_writer = csv.DictWriter(outfile, keys)
            dict_writer.writeheader()
            dict_writer.writerows(forecast_hourly_data_dict_list)
        self.log.info('Wrote response to {}'.format(rendered_csv_output_filepath))
