import argparse
import datetime
from astral import LocationInfo
from astral.sun import sun
import csv
import random
import pytz

# fmt: off
def calculate_sun_times(date, latitude, longitude):
    """
    Getting the sunrise and sunset times for a given date and location. With that calculating different time ranges around sunrise and sunset.
    Returning with dictionary with the calculated time ranges.
    """

    city = LocationInfo("","","UTC",latitude, longitude)
    s = sun(city.observer, date=date, tzinfo=city.timezone)
    s_next = sun(city.observer, date=date + datetime.timedelta(days=1), tzinfo=city.timezone)


    sunrise = s['sunrise']
    sunrise_next = s_next['sunrise']
    sunset = s['sunset']
    
    
    # Nocturnal time ranges
    nocturnal_start_time =   sunset + datetime.timedelta(seconds=5400)
    nocturnal_end_time =  sunrise_next - datetime.timedelta(seconds=5400)

    # Sunrise time ranges
    sunrise_start_time = sunrise - datetime.timedelta(seconds=3600)
    sunrise_end_time = sunrise + datetime.timedelta(seconds=18000)

    
    # Daytime time ranges
    daytime_start_time = sunrise + datetime.timedelta(seconds=19800) 
    daytime_end_time = sunset - datetime.timedelta(seconds=3600)
    
    # Dusk time ranges
    dusk_start_time = sunset - datetime.timedelta(seconds=3600)
    dusk_end_time = sunset + datetime.timedelta(seconds=5040)
    
    return {
        
        "nocturnal_start_time": nocturnal_start_time,
        "nocturnal_end_time": nocturnal_end_time,
        "sunrise_start_time": sunrise_start_time,
        "sunrise_end_time": sunrise_end_time,
        "daytime_start_time": daytime_start_time,
        "daytime_end_time": daytime_end_time,
        "dusk_start_time": dusk_start_time,
        "dusk_end_time": dusk_end_time,
        "sunrise": sunrise,
        "sunset": sunset,
        "sunrise_next": sunrise_next,
    }
    



def datetime_range(start, end, delta):
    """
    Creating a list of datetime objects between two given datetime objects with a given delta.
    """
    current = start
    
    if start <= end:
        while current <= end:
            yield current
            current += delta


def create_date_times_list(date_range, result, user_start_date, user_end_date):
    """
    Generate a list of date times for different time ranges based on the given range of dates and result. Result is a dictionary with the calculated time ranges.
    This function iterates through the input date_range and result, creating lists of date times for
    various time ranges such as night times, sunrise times, daytime times, and sunset times.
    The date times are then combined into a single DataFrame with additional information such as
    Site, ExtFormat, and Filename.
    """
    final_result = []

    for _, res in zip(date_range, result):
        
        nocturnal_times_list = list(
            datetime_range(
                res["nocturnal_start_time"], res["nocturnal_end_time"], datetime.timedelta(seconds=1800)
            )
        )
        
        sunrise_times_list = list(
            datetime_range(
                res["sunrise_start_time"], res["sunrise_end_time"], datetime.timedelta(seconds=1800)
            )
        )
        
        daytime_times_list = list(
            datetime_range(
                res["daytime_start_time"], res["daytime_end_time"], datetime.timedelta(seconds=1800)
            )
        )
        
        dusk_times_list = list(
            datetime_range(
                res["dusk_start_time"], res["dusk_end_time"], datetime.timedelta(seconds=1800)
            )
        )

        # fmt: off
        merged_timings = nocturnal_times_list + sunrise_times_list + daytime_times_list + dusk_times_list
        
        for timing in merged_timings:
            
            # Check if the timing is within the user-defined start and end dates
            if user_start_date <= timing <= user_end_date:
            
                data_dict = {
                    "site": "Site1",
                    "NewDate": timing,
                    "sampleFile": timing.strftime("%Y%m%d_%H%M%S") + ".wav",
                    "sunrise": res["sunrise"],
                    "sunset": res["sunset"],
                    "sunrise_next": res["sunrise_next"]
                }
                final_result.append(data_dict)

    return final_result


# Define time categories based on conditions
def assign_time_category(row):
    """
    Assign a time category to each row of a DataFrame based on the 'NewDate' column.
    This function takes a DataFrame row containing 'NewDate', 'sunrise', and 'sunset' columns,
    and assigns a time category based on the current time, sunrise, and sunset times. The time
    categories include 'EarlyAM', 'MidAM', 'LateAM', 'Nocturnal', 'Dusk', and 'Daytime'.
    """
    
    sunrise = row["sunrise"]
    sunset = row["sunset"]
    current_time = row["NewDate"]
    sunrise_next = row["sunrise_next"]

    
    if current_time >= sunrise - datetime.timedelta(seconds=3900) and current_time <= sunrise + datetime.timedelta(seconds=3594):
        return "EarlySunrise"
    elif current_time > sunrise + datetime.timedelta(seconds=3594) and current_time <= sunrise + datetime.timedelta(seconds=8994):
        return "MidSunrise"
    elif current_time > sunrise + datetime.timedelta(seconds=8994) and current_time <= sunrise + datetime.timedelta(seconds=17994):
        return "LateSunrise"
    elif current_time > sunrise + datetime.timedelta(seconds=17995) and current_time < sunset - datetime.timedelta(seconds=3600):
        return "Daytime"
    elif current_time >= sunset - datetime.timedelta(seconds=3600) and current_time <= sunset + datetime.timedelta(seconds=5400):
        return "Dusk"
    elif current_time > sunset + datetime.timedelta(seconds=600) and current_time < sunrise_next - datetime.timedelta(seconds=3894):
        return "Nocturnal"
    else:
        return "Nocturnal"

# Function to create random samples per category
def create_random_samples(combined_timings, sample_size):
    """
    Generates the random samples for each category based on the sample size. 
    If the sample size is greater than the number of samples in a category, it will print a message and stop the execution.
    """
    
    for row in combined_timings:
        del row["sunrise_next"]
        del row["NewDate"]
        
    category_samples = {}
    
    for row in combined_timings:
        category = row["category"]
        if category not in category_samples:
            category_samples[category] = []
        category_samples[category].append(row)

    random_samples = []
    for category, samples in category_samples.items():
        
        if sample_size is None:
            random_samples.extend(samples)
        
        elif len(samples) < sample_size:
            print(f"Please have smaller sample size for the desired dates mentioned.")
            break
        
        else:
            random_samples.extend(random.sample(samples, sample_size))

    return random_samples


latitude = 40.7128
longitude = -74.0060
sample_size = 5


user_start_date = pytz.timezone("UTC").localize(datetime.datetime.strptime("2023-06-12", "%Y-%m-%d"))
start_date = user_start_date - datetime.timedelta(days=1)

user_end_date = pytz.timezone("UTC").localize(datetime.datetime.strptime("2023-07-12", "%Y-%m-%d"))
end_date = user_end_date + datetime.timedelta(days=1)

date_range = [start_date + datetime.timedelta(days=day) for day in range((end_date - start_date).days + 1)]
sun_times = [calculate_sun_times(date, latitude, longitude) for date in date_range]

combined_timings = create_date_times_list(date_range, sun_times, user_start_date, end_date)


# Adding category to each dictionary in the list
for row in combined_timings:
    row["category"] = assign_time_category(row)
    
# Generate random samples per category
random_samples = create_random_samples(combined_timings, sample_size)
