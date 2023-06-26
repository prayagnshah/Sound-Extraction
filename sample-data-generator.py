import pandas as pd
from datetime import datetime, timedelta
from suncalc import get_times
from astral import LocationInfo
from astral.sun import sun
import pytz


def calculate_sun_times(date, latitude, longitude):
    sun_times = get_times(date, latitude, longitude)

    boss_night_start = sun_times["sunrise"] - timedelta(seconds=18000)
    boss_night_end = sun_times["sunrise"] - timedelta(seconds=7200)

    boss_rise3a_start = sun_times["sunrise"] - timedelta(seconds=1800)
    boss_rise3a_end = sun_times["sunrise"] + timedelta(seconds=16200)

    boss_rise10_start = sun_times["sunrise"] - timedelta(seconds=600)
    boss_rise10_end = sun_times["sunrise"] - timedelta(seconds=600)

    boss_rise_3b_start = sun_times["sunrise"] - timedelta(seconds=3600)
    boss_rise3b_end = sun_times["sunrise"] + timedelta(seconds=18000)

    boss_sunset_start = sun_times["sunset"] - timedelta(seconds=1800)
    boss_sunset_end = sun_times["sunset"] + timedelta(seconds=5400)

    boss_set_start = sun_times["sunset"] - timedelta(seconds=3600)
    boss_set_end = sun_times["sunset"] + timedelta(seconds=3600)

    daytime_set_start = sun_times["sunrise"] + timedelta(seconds=19800)
    daytime_set_end = sun_times["sunset"] - timedelta(seconds=3600)

    # before_sunset_start = sun_times["sunrise"] - timedelta(seconds=32400)
    # after_sunset_end = sun_times["sunrise"] - timedelta(seconds=25200)

    # # print(before_sunset_start, after_sunset_end)

    return {
        "boss_night_start": boss_night_start,
        "boss_night_end": boss_night_end,
        "boss_rise3a_start": boss_rise3a_start,
        "boss_rise3a_end": boss_rise3a_end,
        "boss_rise10_start": boss_rise10_start,
        "boss_rise10_end": boss_rise10_end,
        "boss_rise_3b_start": boss_rise_3b_start,
        "boss_rise3b_end": boss_rise3b_end,
        "boss_sunset_start": boss_sunset_start,
        "boss_sunset_end": boss_sunset_end,
        "boss_set_start": boss_set_start,
        "boss_set_end": boss_set_end,
        "daytime_set_start": daytime_set_start,
        "daytime_set_end": daytime_set_end,
        # "before_sunset_start": before_sunset_start,
        # "after_sunset_end": after_sunset_end,
    }


# Function to create a list of datetimes
def datetime_range(start, end, delta):
    current = start
    while current <= end:
        yield current
        current += delta


def create_date_times_list(date_range, result):
    final_result = []

    for date, res in zip(date_range, result):
        boss_night_times = list(
            datetime_range(
                res["boss_night_start"], res["boss_night_end"], timedelta(seconds=3600)
            )
        )
        # print(boss_night_times)

        boss_rise3a_times = list(
            datetime_range(
                res["boss_rise3a_start"],
                res["boss_rise3a_end"],
                timedelta(seconds=3600),
            )
        )
        boss_rise10_times = list(
            datetime_range(
                res["boss_rise10_start"], res["boss_rise10_end"], timedelta(days=1)
            )
        )
        boss_rise3b_times = list(
            datetime_range(
                res["boss_rise_3b_start"],
                res["boss_rise3b_end"],
                timedelta(seconds=3600),
            )
        )
        daytime_times = list(
            datetime_range(
                res["daytime_set_start"],
                res["daytime_set_end"],
                timedelta(seconds=3600),
            )
        )
        boss_sunset_times = list(
            datetime_range(
                res["boss_sunset_start"],
                res["boss_sunset_end"],
                timedelta(seconds=3600),
            )
        )
        # print(boss_sunset_times)
        boss_set_times = list(
            datetime_range(
                res["boss_set_start"], res["boss_set_end"], timedelta(seconds=3600)
            )
        )

        # before_sunset_times = list(
        #     datetime_range(
        #         res["before_sunset_start"],
        #         res["after_sunset_end"],
        #         timedelta(seconds=1800),
        #     )
        # )
        # print(before_sunset_times)

        # fmt: off
        boss_table = boss_night_times + boss_rise3a_times + boss_rise10_times + boss_rise3b_times + boss_sunset_times + boss_set_times + daytime_times
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
    location = LocationInfo(latitude=latitude, longitude=longitude)

    # Convert NewDate to datetime
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
            seconds=3900
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
        if current_time >= sunset - timedelta(
            seconds=4200
        ) and current_time <= sunset + timedelta(seconds=600):
            return "Dusk"
        elif current_time >= sunrise + timedelta(
            seconds=19800
        ) and current_time < sunset - timedelta(seconds=4500):
            return "Daytime"

        elif (
            # Check if current time is after sunset and before midnight
            (
                current_time >= sunset + timedelta(seconds=5400)
                and current_time <= sunset.replace(hour=23, minute=59, second=59)
            )
            or
            # Check if current time is after midnight and before sunrise
            (
                current_time >= sunset.replace(hour=0, minute=0, second=0)
                and current_time <= sunrise - timedelta(seconds=3600)
            )
        ):
            return "Nocturnal"


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
