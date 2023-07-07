import pandas as pd
import argparse
from datetime import timedelta
from suntime import Sun

# fmt: off
def calculate_sun_times(date, latitude, longitude):
    """
    Getting the sunrise and sunset times for a given date and location. With that calculating different time ranges around sunrise and sunset.
    Returning with dictionary with the calculated time ranges.
    """

    sun = Sun(latitude, longitude)
    # sun_times = suncalc.get_times(date, latitude, longitude)
    sunrise = sun.get_local_sunrise_time(date)
    sunset = sun.get_local_sunset_time(date)
    # print("Sunrise: ", sunrise)
    # print("Sunset: ", sunset)

    
    # Nocturnal time ranges
    nocturnal_start_time =   sunset + timedelta(seconds=5400)
    nocturnal_end_time =  sunrise - timedelta(seconds=5400)
    # print("Nocturnal time ranges: ", nocturnal_start_time, nocturnal_end_time)
    
    sunrise_start_time = sunrise - timedelta(seconds=3600)
    sunrise_end_time = sunrise + timedelta(seconds=18000)
    # print("Sunrise time ranges: ", sunrise_start_time, sunrise_end_time)
    
    daytime_start_time = sunrise + timedelta(seconds=19800) 
    daytime_end_time = sunset - timedelta(seconds=3600)
    
    dusk_start_time = sunset - timedelta(seconds=3600)
    dusk_end_time = sunset + timedelta(seconds=5040)


    return {
        
        "nocturnal_start_time": nocturnal_start_time,
        "nocturnal_end_time": nocturnal_end_time,
        "sunrise_start_time": sunrise_start_time,
        "sunrise_end_time": sunrise_end_time,
        "daytime_start_time": daytime_start_time,
        "daytime_end_time": daytime_end_time,
        "dusk_start_time": dusk_start_time,
        "dusk_end_time": dusk_end_time,
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
    else:
        while current <= end + timedelta(days=1):
            yield current
            current += delta    


def create_date_times_list(date_range, result):
    """
    Generate a list of date times for different time ranges based on the given range of dates and result. Result is a dictionary with the calculated time ranges.
    This function iterates through the input date_range and result, creating lists of date times for
    various time ranges such as night times, sunrise times, daytime times, and sunset times.
    The date times are then combined into a single DataFrame with additional information such as
    Site, ExtFormat, and Filename.
    """
    final_result = []

    for date, res in zip(date_range, result):
        
        nocturnal_times_list = list(
            datetime_range(
                res["nocturnal_start_time"], res["nocturnal_end_time"], timedelta(seconds=1800)
            )
        )
        # print(nocturnal_times_list)
        
        sunrise_times_list = list(
            datetime_range(
                res["sunrise_start_time"], res["sunrise_end_time"], timedelta(seconds=1800)
            )
        )
        # print(sunrise_times_list)
        
        daytime_times_list = list(
            datetime_range(
                res["daytime_start_time"], res["daytime_end_time"], timedelta(seconds=1800)
            )
        )
        
        dusk_times_list = list(
            datetime_range(
                res["dusk_start_time"], res["dusk_end_time"], timedelta(seconds=1800)
            )
        )
        
        # print(f"Nocturnal: {res['nocturnal_start_time']} - {res['nocturnal_end_time']}")
        # print(f"Sunrise: {res['sunrise_start_time']} - {res['sunrise_end_time']}")
        # print(f"Daytime: {res['daytime_start_time']} - {res['daytime_end_time']}")
        # print(f"Dusk: {res['dusk_start_time']} - {res['dusk_end_time']}")
        
        # print("Nocturnal times: ", nocturnal_times_list)
        # print("Sunrise times: ", sunrise_times_list)
        # print("Daytime times: ", daytime_times_list)
        # print("Dusk times: ", dusk_times_list)
        # print(dusk_times_list)
        

        # fmt: off
        merged_timings = nocturnal_times_list + sunrise_times_list + daytime_times_list + dusk_times_list

        merged_timings_df = pd.DataFrame({"date_time": merged_timings})
        # print(merged_timings_df)
        merged_timings_df["Site"] = "SandPond192450"
        merged_timings_df["ExtFormat"] = "wav"
        merged_timings_df["NewDate"] = merged_timings_df["date_time"].dt.strftime("%Y%m%d_%H%M%S")
        merged_timings_df["sampleFile"] = (
            merged_timings_df["Site"]
            + "_"
            + merged_timings_df["NewDate"]
            + "."
            + merged_timings_df["ExtFormat"]
        )

        merged_timings_df = merged_timings_df.drop(["date_time"], axis=1)
        final_result.append(merged_timings_df)
    var = pd.concat(final_result, ignore_index=True) 
    # print(var)
    return var


def calculate_sunrise_sunset(df, latitude, longitude):
    """
    Calculate sunrise and sunset times for each date in the input DataFrame.
    This function takes a DataFrame containing a 'NewDate' column with date-time values, and
    calculates the corresponding sunrise and sunset times for each date based on the provided
    latitude and longitude. The resulting sunrise and sunset times are then added as new columns
    to the input DataFrame.
    """
    # location = LocationInfo(latitude=latitude, longitude=longitude)
    sun = Sun(latitude, longitude)

    df["NewDate"] = pd.to_datetime(df["NewDate"], format="%Y%m%d_%H%M%S")

    df["sunrise"] = df["NewDate"].apply(
        lambda x: sun.get_local_sunrise_time(x.date())
    )
    df["sunset"] = df["NewDate"].apply(
        lambda x: sun.get_local_sunset_time(x.date())
    )
    df["sunrise"] = (
        df["sunrise"]
        .dt.tz_localize(None)
    )
    df["sunset"] = (
        df["sunset"]
        .dt.tz_localize(None)
    )

    df = df.drop_duplicates(subset=["NewDate"], keep="first")
    
    return df


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

    # print(
    #     f"Sunset: {row['sunset']}, Sunrise: {row['sunrise']}, Current Time: {row['NewDate']}"
    # )
    
    if current_time >= sunrise - timedelta(seconds=3900) and current_time <= sunrise + timedelta(seconds=3594):
        return "EarlyAM"
    elif current_time > sunrise + timedelta(seconds=3594) and current_time <= sunrise + timedelta(seconds=8994):
        return "MidAM"
    elif current_time > sunrise + timedelta(seconds=8994) and current_time <= sunrise + timedelta(seconds=17994):
        return "LateAM"
    elif current_time > sunrise + timedelta(seconds=17994) and current_time < sunset - timedelta(seconds=3600):
        return "Daytime"
    elif current_time >= sunset - timedelta(seconds=3600) and current_time <= sunset + timedelta(seconds=5400):
        return "Dusk"
    elif current_time >= sunset + timedelta(seconds=600) or current_time <= sunrise - timedelta(seconds=3894):
        return "Nocturnal"
    else:
        return "NULL"


    # if current_time > sunrise - timedelta(
    #     seconds=3900
    # ) and current_time <= sunrise + timedelta(seconds=3594):
    #     return "EarlyAM"
    # elif current_time >= sunrise + timedelta(
    #     seconds=3600
    # ) and current_time <= sunrise + timedelta(seconds=8994):
    #     return "MidAM"
    # elif current_time > sunrise + timedelta(
    #     seconds=9000
    # ) and current_time <= sunrise + timedelta(seconds=17994):
    #     return "LateAM"
    #     # else:
    #     #     return "Nocturnal"

    # elif current_time > sunset - timedelta(
    #         seconds=4200
    #     ) and current_time <= sunset + timedelta(seconds=594):
    #         return "Dusk"
    # elif current_time > sunrise + timedelta(
    #     seconds=18000
    # ) and current_time <= sunset - timedelta(seconds=4206):
    #     return "Daytime"

    # elif current_time > sunrise - timedelta(seconds=3600) and current_time <= sunset + timedelta(seconds=600):
    #     return "Nocturnal"
    
    # else:
    #     return "NULL"


parser = argparse.ArgumentParser(
    description="Generating random samples from a list of date-times"
)

parser.add_argument('--latitude', type=float, required=True, help='Latitude of the site')
parser.add_argument('--longitude', type=float, help='Longitude of the site')
parser.add_argument('--start_date', type=str, help='Start date of the sampling period')
parser.add_argument('--end_date', type=str, help='End date of the sampling period')
parser.add_argument('--sample_size', type=int, help='Number of samples per category')

args = parser.parse_args()

# Calling the variables and functions

latitude = args.latitude
longitude = args.longitude
start_date = pd.to_datetime(args.start_date)
end_date = pd.to_datetime(args.end_date)
date_range = pd.date_range(start_date, end_date, freq="D")
sun_times = [calculate_sun_times(date, latitude, longitude) for date in date_range]
final_result = create_date_times_list(date_range, sun_times)
combined_timings = calculate_sunrise_sunset(final_result, latitude, longitude)
combined_timings["category"] = combined_timings.apply(assign_time_category, axis=1)
# print(combined_timings)
combined_timings.to_csv("sample-data.csv", date_format='%Y-%m-%d %H:%M:%S', index=False)
sample_size = args.sample_size  # Change this value to the desired number of samples per category
random_samples = combined_timings.groupby("category").apply(
    lambda x: x.sample(sample_size)
)

# Reset index
random_samples.reset_index(drop=True, inplace=True)
# random_samples.to_csv("sample-data.csv", index=False)
print(random_samples)