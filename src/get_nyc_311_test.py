import pandas as pd
from sodapy import Socrata
import json

NYC_OPEN_DATA_ENPOINT = 'data.cityofnewyork.us'
NYC_311_ENDPOINT = 'fhrw-4uyv'
SOCRATA_APP_TOKEN = 'uIFjyIVrXUIML1KO9hU1B4dmF'

# Example authenticated client (needed for non-public datasets):
client = Socrata(NYC_OPEN_DATA_ENPOINT,
                 SOCRATA_APP_TOKEN)

# First 2000 results, returned as JSON from API

results = client.get(NYC_311_ENDPOINT, where="closed_date between '2019-10-13' and '2019-10-14'", limit=2000, exclude_system_fields=False)

# write out as json
with open('noise_complaints_311.json', 'w') as outfile:
    json.dump(results, outfile)

# read json as pandas
results_df= pd.read_json('noise_complaints_311.json')
print(results_df)
print('-'*10)

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)
print(results_df)

# Write results
results_df.to_csv('noise_complaints_311.csv', index=False)
