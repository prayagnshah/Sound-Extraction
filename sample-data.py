import csv
from datetime import datetime, timedelta
from suntime import Sun, SunTimeException
import pandas as pd

# latitude and longitude
lat, lon = 43.815463, -65.840105

# date range
start_date = '2022-5-7'
end_date = '2022-5-9'

# list to hold the data
data = []

# setup Sun
sun = Sun(lat, lon)

# convert start_date and end_date to datetime and add one day to end_date
start_date = datetime.strptime(start_date, "%Y-%m-%d")
end_date = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)


# function to categorize timestamps
def categorize_time(current_time, sunrise, sunset):
    if current_time >= sunrise - timedelta(seconds=3900) and current_time <= sunrise + timedelta(seconds=3594):
        return "EarlySunrise"
    elif current_time > sunrise + timedelta(seconds=3594) and current_time <= sunrise + timedelta(seconds=8994):
        return "MidSunrise"
    elif current_time > sunrise + timedelta(seconds=8994) and current_time <= sunrise + timedelta(seconds=17994):
        return "LateSunrise"
    elif current_time > sunrise + timedelta(seconds=17994) and current_time < sunset - timedelta(seconds=3600):
        return "Daytime"
    elif current_time >= sunset - timedelta(seconds=3600) and current_time <= sunset + timedelta(seconds=5400):
        return "Dusk"
    elif current_time > sunset + timedelta(seconds=600) or current_time < sunrise - timedelta(seconds=3894):
        return "Nocturnal"
    else:
        return "NULL"

# iterate over the range of dates
for date in pd.date_range(start_date, end_date):
    # get sunrise and sunset times
    sunrise = sun.get_local_sunrise_time(date)
    sunset = sun.get_local_sunset_time(date)
    
    # generate timestamps every 30 minutes between sunrise and sunset
    timestamps = pd.date_range(date, date + timedelta(days=1), freq='30T', tz= 'UTC')
    
    # add each timestamp to data
    for ts in timestamps:
        # append latitude, longitude, and the timestamp
        data.append([lat, lon, ts, categorize_time(ts, sunrise, sunset)])

# write data to csv
with open('output.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Latitude", "Longitude", "Timestamp", "Category"])  # write the header
    writer.writerows(data)  # write the data