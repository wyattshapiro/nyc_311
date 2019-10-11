import pandas as pd
from sodapy import Socrata

NYC_OPEN_DATA_ENPOINT = 'data.cityofnewyork.us'
NYC_311_ENDPOINT = 'fhrw-4uyv'
SOCRATA_APP_TOKEN = 'uIFjyIVrXUIML1KO9hU1B4dmF'

# Example authenticated client (needed for non-public datasets):
client = Socrata(NYC_OPEN_DATA_ENPOINT,
                 SOCRATA_APP_TOKEN)

# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
results = client.get(NYC_311_ENDPOINT, where='starts_with(complaint_type, "Noise")', limit=50000, exclude_system_fields=False)

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)

# Write results
results_df.to_csv('noise_complaints_311.csv', index=False)
