from datetime import datetime, timedelta, timezone
from astral import LocationInfo
from astral.sun import sun
import csv
import pytz

def generate_sample_data(start_date, end_date, latitude, longitude):
    
        
    # Create a timezone object for 'America/Halifax'
    halifax_tz = pytz.timezone('America/Halifax')
    
    hours = 4.95
    seconds = hours * 3600
    
    
    
 
    # Calculate sunrise and sunset times using suntime library
    location_info = LocationInfo("","","UTC",latitude, longitude)
    
    # print(location_info)
    
    recordings = []
    
    current_time = start_date
    while current_time <= end_date:
        recordings.append(current_time)
        current_time += timedelta(minutes=30)
    
    categorized_recordings = []
    
    # print(recordings)
    
    for current_time in recordings:
        
        s = sun(location_info.observer, date=current_time.date())
        sunrise = s['sunrise']  
        sunset = s['sunset']
        # print(sunset > sunrise)
        
        # Calculate sunrise time for the next day
        next_day_sunrise = sun(location_info.observer,date=(current_time + timedelta(days=1)).date())
        next_day = next_day_sunrise['sunrise']
        
        # next_day_sunset = sun.get_sunset_time((recording + timedelta(days=1)).date())
        # print(next_day_sunset)
        
        if current_time >= sunrise - timedelta(seconds=3900) and current_time <= sunrise + timedelta(seconds=3594):
            category = "EarlySunrise"
        elif current_time > sunrise + timedelta(seconds=3594) and current_time<= sunrise + timedelta(seconds=8994):
            category = "MidSunrise"
        elif current_time > sunrise + timedelta(seconds=8994) and current_time <= sunrise + timedelta(seconds=17994):
            category = "LateSunrise"
        elif current_time >= sunrise + timedelta(seconds=17995) or current_time < sunset - timedelta(seconds=3600):
            category = "Daytime"
        elif current_time >= sunset - timedelta(seconds=3600) and current_time <= sunset + timedelta(seconds=5400):
            category = "Dusk"
        elif current_time > sunset + timedelta(seconds=600) or current_time < next_day - timedelta(seconds=3894):
            category = "Nocturnal"
        else:
            category = "NULL"
                
        categorized_recordings.append((current_time, category))
    
    # Convert the timezone of each datetime object
    categorized_recordings = [(dt.astimezone(halifax_tz), category) for dt, category in categorized_recordings]
    print(categorized_recordings)
        
    return categorized_recordings

def write_to_csv(categorized_recordings, filename):
    with open('sample-data.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["sampleName", "Category"])  # write the header


        for recording in categorized_recordings:
            time_str = recording[0].strftime("%Y%m%d_%H%M%S")
            writer.writerow([time_str, recording[1]])
            



start_date = datetime(2021,7,5, tzinfo=timezone.utc)
end_date = datetime(2021,7,10, tzinfo=timezone.utc)
latitude = 43.815463
longitude = -65.840105


sample_data = generate_sample_data(start_date, end_date, latitude, longitude)

write_to_csv(sample_data, "sample-data.csv")


# for recording, category in sample_data:
#     print(f"Recording: {recording} , Category: {category}")

# latitude = 43.815463
# longitude = -65.840105