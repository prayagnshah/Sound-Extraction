import pandas as pd
from datetime import datetime, timedelta
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

    night_start_time = sunrise - timedelta(seconds=18000)  # Night starts 5 hours before sunrise
    night_end_time = sunrise - timedelta(seconds=7200)     # Night ends 2 hours before sunrise

    sunrise_rise3a_start_time = sunrise - timedelta(seconds=1800)  # 30 minutes before sunrise
    sunrise_rise3a_end_time = sunrise + timedelta(seconds=16200)   # 4.5 hours after sunrise

    sunrise_rise10_start_time = sunrise - timedelta(seconds=600)  # 10 minutes before sunrise
    sunrise_rise10_end_time = sunrise - timedelta(seconds=600)    # 10 minutes before sunrise

    sunrise_rise3b_start_time = sunrise - timedelta(seconds=3600) # 1 hour before sunrise
    sunrise_rise3b_end_time = sunrise + timedelta(seconds=18000)  # 5 hours after sunrise

    sunset_start_time = sunset - timedelta(seconds=1800)    # 30 minutes before sunset
    sunset_end_time = sunset + timedelta(seconds=5400)      # 1.5 hours after sunset

    boss_set_start = sunset - timedelta(seconds=3600)       # 1 hour before sunset
    boss_set_end = sunset + timedelta(seconds=3600)         # 1 hour after sunset

    daytime_start_time = sunrise + timedelta(seconds=19800)     # 5.5 hours after sunrise
    daytime_end_time = sunset - timedelta(seconds=3600)         # 1 hour before sunset

    sunset_before_start_time = sunrise - timedelta(seconds=36000) # 10 hours before sunrise
    sunset_after_end_time = sunrise - timedelta(seconds=27000)    # 7.5 hours before sunrise

    # # print(sunset_before_start_time, sunset_after_end_time)

    return {
        "night_start_time": night_start_time,
        "night_end_time": night_end_time,
        "sunrise_rise3a_start_time": sunrise_rise3a_start_time,
        "sunrise_rise3a_end_time": sunrise_rise3a_end_time,
        "sunrise_rise10_start_time": sunrise_rise10_start_time,
        "sunrise_rise10_end_time": sunrise_rise10_end_time,
        "sunrise_rise3b_start_time": sunrise_rise3b_start_time,
        "sunrise_rise3b_end_time": sunrise_rise3b_end_time,
        "sunset_start_time": sunset_start_time,
        "sunset_end_time": sunset_end_time,
        "boss_set_start": boss_set_start,
        "boss_set_end": boss_set_end,
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
        boss_night_times = list(
            datetime_range(
                res["night_start_time"], res["night_end_time"], timedelta(seconds=3600)
            )
        )
        # print(boss_night_times)

        boss_rise3a_times = list(
            datetime_range(
                res["sunrise_rise3a_start_time"],
                res["sunrise_rise3a_end_time"],
                timedelta(seconds=3600),
            )
        )
        boss_rise10_times = list(
            datetime_range(
                res["sunrise_rise10_start_time"],
                res["sunrise_rise10_end_time"],
                timedelta(days=1),
            )
        )
        boss_rise3b_times = list(
            datetime_range(
                res["sunrise_rise3b_start_time"],
                res["sunrise_rise3b_end_time"],
                timedelta(seconds=3600),
            )
        )
        daytime_times = list(
            datetime_range(
                res["daytime_start_time"],
                res["daytime_end_time"],
                timedelta(seconds=3600),
            )
        )
        boss_sunset_times = list(
            datetime_range(
                res["sunset_start_time"],
                res["sunset_end_time"],
                timedelta(seconds=3600),
            )
        )
        # print(boss_sunset_times)
        boss_set_times = list(
            datetime_range(
                res["boss_set_start"], res["boss_set_end"], timedelta(seconds=3600)
            )
        )

        before_sunset_times = list(
            datetime_range(
                res["sunset_before_start_time"],
                res["sunset_after_end_time"],
                timedelta(seconds=1800),
            )
        )
        # print(before_sunset_times)

        # fmt: off
        boss_table = boss_night_times + boss_rise3a_times + boss_rise10_times + boss_rise3b_times + boss_sunset_times + boss_set_times + daytime_times + before_sunset_times
        # print(boss_table)

        boss_table_df = pd.DataFrame({"date_time": boss_table})
        # print(boss_table_df)
        boss_table_df["Site"] = "SandPond192450"
        boss_table_df["ExtFormat"] = "wav"
        boss_table_df["NewDate"] = boss_table_df["date_time"].dt.strftime("%Y%m%d_%H%M%S")
        boss_table_df["Filename"] = (
            boss_table_df["Site"]
            + "_"
            + boss_table_df["NewDate"]
            + "."
            + boss_table_df["ExtFormat"]
        )

        final_result.append(boss_table_df)

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
    categories include 'EE- Early Breeding', 'EM- Early Mid-Breeding', 'EL-Early Late Breeding', 'Nocturnal', 'Dusk', and 'Daytime'.
    """
    early_start = pd.Timestamp("2021-07-01")
    early_end = pd.Timestamp("2021-08-25")

    sunrise = row["sunrise"]
    sunset = row["sunset"]
    current_time = row["NewDate"]

    # print(
    #     f"Sunset: {row['sunset']}, Sunrise: {row['sunrise']}, Current Time: {row['NewDate']}"
    # )

    if early_start <= current_time <= early_end:
        if current_time >= sunrise - timedelta(
            seconds=5000
        ) and current_time <= sunrise + timedelta(seconds=2940):
            return "EE"
        elif current_time > sunrise + timedelta(
            seconds=3000
        ) and current_time <= sunrise + timedelta(seconds=9000):
            return "EM"
        elif current_time > sunrise + timedelta(
            seconds=9036
        ) and current_time <= sunrise + timedelta(seconds=19000):
            return "EL"
        else:
            return "Nocturnal"

    else:
        if current_time >= sunset - timedelta(
            seconds=4200
        ) and current_time <= sunset + timedelta(seconds=600):
            return "Dusk"
        elif current_time >= sunrise + timedelta(
            seconds=19800
        ) and current_time < sunset - timedelta(seconds=4500):
            return "Daytime"

        elif (
            (
                current_time >= sunset + timedelta(seconds=5400)
                and current_time <= sunset.replace(hour=23, minute=59, second=59)
            )
            or
            (
                current_time >= sunset.replace(hour=0, minute=0, second=0)
                and current_time <= sunrise - timedelta(seconds=3600)
            )
        ):
            return "Nocturnal"



# Calling the variables and functions

latitude = 44.720528
longitude = -62.800722
start_date = pd.to_datetime("2021-07-05")
end_date = pd.to_datetime("2021-08-31")
date_range = pd.date_range(start_date, end_date, freq="D", tz="America/Halifax")
sun_times = [calculate_sun_times(date, latitude, longitude) for date in date_range]
final_result = create_date_times_list(date_range, sun_times)
combined_df = calculate_sunrise_sunset(final_result, latitude, longitude)
combined_df["TimeCategory"] = combined_df.apply(assign_time_category, axis=1)
# print(combined_df)
combined_df.to_csv("sample-data.csv", index=False)
sample_size = 4  # Change this value to the desired number of samples per category
random_samples = combined_df.groupby("TimeCategory").apply(
    lambda x: x.sample(sample_size)
)

# Reset index
random_samples.reset_index(drop=True, inplace=True)
# random_samples.to_csv("sample-data.csv", index=False)
# print(random_samples)
