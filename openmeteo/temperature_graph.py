import openmeteo_requests

import pandas as pd
import matplotlib.pyplot as plt
import requests_cache
from retry_requests import retry

# Set up the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession(".cache", expire_after=-1)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://archive-api.open-meteo.com/v1/archive"
params = {
    "latitude": 51.1027,
    "longitude": 16.8858,
    "start_date": "2000-01-01",
    "end_date": "2025-12-31",
    "hourly": "temperature_2m",
}
responses = openmeteo.weather_api(url, params=params)

# Process first location
response = responses[0]
print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation: {response.Elevation()} m asl")
print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

# Process hourly data. The order of variables needs to be the same as requested.
hourly = response.Hourly()
hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

hourly_data = {
    "date": pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left",
    ),
    "temperature_2m": hourly_temperature_2m,
}

hourly_dataframe = pd.DataFrame(data=hourly_data)
print("\nHourly data\n", hourly_dataframe)

plt.figure(figsize=(12, 12))
plt.plot(
    hourly_dataframe["date"], hourly_dataframe["temperature_2m"], label="temperature_2m"
)
plt.xlabel("Date")
plt.ylabel("Temperature at 2m (°C)")
plt.title("Temperature at 2m over time")
plt.legend()
plt.grid()
plt.savefig("temperature_2m_hourly.png")
