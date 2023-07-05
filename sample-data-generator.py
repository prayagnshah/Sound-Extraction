import pandas as pd
import argparse
from datetime import timedelta
from suncalc import get_times
from astral import LocationInfo
from astral.sun import sun
import pytz

# fmt: off
def calculate_sun_times(date, latitude, longitude):
    """
    Getting the sunrise and sunset times for a given date and location. With that calculating different time ranges around sunrise and sunset.
    Returning with dictionary with the calculated time ranges.
    """

    sun_times = get_times(date, latitude, longitude)
    sunrise = sun_times["sunrise"]
    sunset = sun_times["sunset"]

    night_start_time = sunrise - timedelta(seconds=21600)  # Night starts 6 hours before sunrise
    night_end_time = sunrise - timedelta(seconds=7200)     # Night ends 2 hours before sunrise

    sunrise_rise3a_start_time = sunrise - timedelta(seconds=1800)  # 30 minutes before sunrise
    sunrise_rise3a_end_time = sunrise + timedelta(seconds=16200)   # 4.5 hours after sunrise

    sunrise_rise3b_start_time = sunrise - timedelta(seconds=3600) # 1 hour before sunrise
    sunrise_rise3b_end_time = sunrise + timedelta(seconds=18000)  # 5 hours after sunrise

    sunset_start_time = sunset - timedelta(seconds=1800)    # 30 minutes before sunset
    sunset_end_time = sunset + timedelta(seconds=5400)      # 1.5 hours after sunset

    # boss_set_start = sunset - timedelta(seconds=3600)       # 1 hour before sunset
    # boss_set_end = sunset + timedelta(seconds=3600)         # 1 hour after sunset

    daytime_start_time = sunrise + timedelta(seconds=19800)       # 5.5 hours after sunrise
    daytime_end_time = sunrise + timedelta(seconds=48600)         # 13.5 hours after sunrise

    sunset_before_start_time = sunset - timedelta(seconds=3600) # 10 hours before sunrise
    sunset_after_end_time = sunset - timedelta(seconds=5400)    # 7.5 hours before sunrise

    # # print(sunset_before_start_time, sunset_after_end_time)

    return {
        "night_start_time": night_start_time,
        "night_end_time": night_end_time,
        "sunrise_rise3a_start_time": sunrise_rise3a_start_time,
        "sunrise_rise3a_end_time": sunrise_rise3a_end_time,
        "sunrise_rise3b_start_time": sunrise_rise3b_start_time,
        "sunrise_rise3b_end_time": sunrise_rise3b_end_time,
        "sunset_start_time": sunset_start_time,
        "sunset_end_time": sunset_end_time,
        # "boss_set_start": boss_set_start,
        # "boss_set_end": boss_set_end,
        "daytime_start_time": daytime_start_time,
        "daytime_end_time": daytime_end_time,
        "sunset_before_start_time": sunset_before_start_time,
        "sunset_after_end_time": sunset_after_end_time,
    }



def datetime_range(start, end, delta):
    """
    Creating a list of datetime objects between two given datetime objects with a given delta.
    """
    current = start
    while current <= end:
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
        night_times_list = list(
            datetime_range(
                res["night_start_time"], res["night_end_time"], timedelta(seconds=3600)
            )
        )
        # print(night_times_list)

        sunrise3a_times_list = list(
            datetime_range(
                res["sunrise_rise3a_start_time"],
                res["sunrise_rise3a_end_time"],
                timedelta(seconds=3600),
            )
        )
        sunrise3b_times_list = list(
            datetime_range(
                res["sunrise_rise3b_start_time"],
                res["sunrise_rise3b_end_time"],
                timedelta(seconds=3600),
            )
        )
        daytime_times_list = list(
            datetime_range(
                res["daytime_start_time"],
                res["daytime_end_time"],
                timedelta(seconds=3600),
            )
        )
        # print(daytime_times_list)
        sunset_times_list = list(
            datetime_range(
                res["sunset_start_time"],
                res["sunset_end_time"],
                timedelta(seconds=3600),
            )
        )
        # print(sunset_times_list)
        # aftersunset_times_list = list(
        #     datetime_range(
        #         res["boss_set_start"], res["boss_set_end"], timedelta(seconds=3600)
        #     )
        # )

        beforesunset_times_list = list(
            datetime_range(
                res["sunset_before_start_time"],
                res["sunset_after_end_time"],
                timedelta(seconds=1800),
            )
        )
        # print(beforesunset_times_list)

        # fmt: off
        merged_timings = night_times_list + sunrise3a_times_list + sunrise3b_times_list + sunset_times_list + daytime_times_list + beforesunset_times_list

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

    return pd.concat(final_result, ignore_index=True)


def calculate_sunrise_sunset(df, latitude, longitude):
    """
    Calculate sunrise and sunset times for each date in the input DataFrame.
    This function takes a DataFrame containing a 'NewDate' column with date-time values, and
    calculates the corresponding sunrise and sunset times for each date based on the provided
    latitude and longitude. The resulting sunrise and sunset times are then added as new columns
    to the input DataFrame.
    """
    location = LocationInfo(latitude=latitude, longitude=longitude)

    df["NewDate"] = pd.to_datetime(df["NewDate"], format="%Y%m%d_%H%M%S")

    df["sunrise"] = df["NewDate"].apply(
        lambda x: sun(location.observer, date=x.date())["sunrise"]
    )
    df["sunset"] = df["NewDate"].apply(
        lambda x: sun(location.observer, date=x.date())["sunset"]
    )
    df["sunrise"] = (
        df["sunrise"]
        .dt.tz_convert(pytz.timezone("America/Halifax"))
        .dt.tz_localize(None)
    )
    df["sunset"] = (
        df["sunset"]
        .dt.tz_convert(pytz.timezone("America/Halifax"))
        .dt.tz_localize(None)
    )
    return df


# Define time categories based on conditions
def assign_time_category(row):
    """
    Assign a time category to each row of a DataFrame based on the 'NewDate' column.
    This function takes a DataFrame row containing 'NewDate', 'sunrise', and 'sunset' columns,
    and assigns a time category based on the current time, sunrise, and sunset times. The time
    categories include 'Early AM', 'MidAM', 'LateAM', 'Nocturnal', 'Dusk', and 'Daytime'.
    """

    sunrise = row["sunrise"]
    sunset = row["sunset"]
    current_time = row["NewDate"]

    # print(
    #     f"Sunset: {row['sunset']}, Sunrise: {row['sunrise']}, Current Time: {row['NewDate']}"
    # )


    if current_time >= sunrise - timedelta(
        seconds=3900
    ) and current_time <= sunrise + timedelta(seconds=3594):
        return "EarlyAM"
    elif current_time > sunrise + timedelta(
        seconds=3600
    ) and current_time <= sunrise + timedelta(seconds=8994):
        return "MidAM"
    elif current_time > sunrise + timedelta(
        seconds=9000
    ) and current_time <= sunrise + timedelta(seconds=17994):
        return "LateAM"
        # else:
        #     return "Nocturnal"

    elif current_time > sunset - timedelta(
            seconds=4200
        ) and current_time <= sunset + timedelta(seconds=594):
            return "Dusk"
    elif current_time > sunrise + timedelta(
        seconds=18000
    ) and current_time <= sunset - timedelta(seconds=4206):
        return "Daytime"

    else:
        return "Nocturnal"


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
date_range = pd.date_range(start_date, end_date, freq="D", tz="America/Halifax")
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