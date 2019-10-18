from darksky.api import DarkSky
from darksky.types import languages, units, weather
import datetime
import csv

API_KEY = '9fb448de3496f51cc78382c7402ea340'

# Synchronous way
darksky = DarkSky(API_KEY)

latitude = 40.730610
longitude = -73.935242
date_time_str = '2018-06-29'
date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d')
forecast = darksky.get_time_machine_forecast(
    latitude, longitude, date_time_obj,
    extend=False,  # default `False`
    lang=languages.ENGLISH,  # default `ENGLISH`
    units=units.AUTO,  # default `auto`
    exclude=[weather.CURRENTLY, weather.MINUTELY, weather.DAILY, weather.ALERTS]  # default `[]`
)

print('-' * 10)
forecast_hourly_data_object_list = forecast.hourly.data
forecast_hourly_data_dict_list = []
for forecast_hourly_data_object in forecast_hourly_data_object_list:
    forecast_hourly_data_dict_list.append(vars(forecast_hourly_data_dict))
rendered_csv_output_filepath = 'nyc_weather_data.csv'
keys = forecast_hourly_data_dict_list[0].keys()
with open(rendered_csv_output_filepath, 'w') as outfile:
    dict_writer = csv.DictWriter(outfile, keys)
    dict_writer.writeheader()
    dict_writer.writerows(forecast_hourly_data_dict_list)
