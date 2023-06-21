import pandas as pd
from datetime import datetime, timedelta
from suncalc import get_times

# Mentioning the start and end date
start_date = pd.to_datetime("2021-07-05")
end_date = pd.to_datetime("2021-07-31")

# coords = pd.read_csv("GPS_log.csv", skiprows=1)
latitude = 44.72
longitude = -62.80

# Create an empty list to store the results of the sunset times
result = []
date_range = pd.date_range(start_date, end_date, freq="D", tz="America/Halifax")

# Loop through the dates and get the sunrise and sunset times
for date in date_range:
    sun_times = get_times(date, latitude, longitude)

    boss_night_start = sun_times["sunrise"] - timedelta(seconds=18000)
    boss_night_end = sun_times["sunrise"] - timedelta(seconds=7200)

    boss_rise3a_start = sun_times["sunrise"] - timedelta(seconds=1800)
    boss_rise3a_end = sun_times["sunrise"] + timedelta(seconds=16200)

    boss_rise10_start = sun_times["sunrise"] - timedelta(seconds=600)
    boss_rise10_end = sun_times["sunrise"] - timedelta(seconds=600)

    boss_rise_3b_start = sun_times["sunrise"] - timedelta(seconds=3600)
    boss_rise3b_end = sun_times["sunset"] + timedelta(seconds=18000)

    boss_sunset_start = sun_times["sunset"] - timedelta(seconds=1800)
    boss_sunset_end = sun_times["sunset"] + timedelta(seconds=5400)

    boss_set_start = sun_times["sunset"] - timedelta(seconds=3600)
    boss_set_end = sun_times["sunset"] + timedelta(seconds=3600)

    daytime_set_start = sun_times["sunset"] + timedelta(seconds=19800)
    daytime_set_end = sun_times["sunset"] - timedelta(seconds=3600)

    result.append(
        {
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
        }
    )


result_df = pd.DataFrame(result)


#
def datetime_range(start, end, delta):
    current = start
    while current <= end:
        yield current
        current += delta


# Create an empty DataFrame to store the final results
final_result = []


# Loop through the results and create a list of datetimes
for date, res in zip(date_range, result):
    boss_night_times = list(
        datetime_range(
            res["boss_night_start"], res["boss_night_end"], timedelta(seconds=3600)
        )
    )

    boss_rise3a_times = list(
        datetime_range(
            res["boss_rise3a_start"], res["boss_rise3a_end"], timedelta(seconds=3600)
        )
    )
    boss_rise10_times = list(
        datetime_range(
            res["boss_rise10_start"], res["boss_rise10_end"], timedelta(days=1)
        )
    )
    boss_rise3b_times = list(
        datetime_range(
            res["boss_rise_3b_start"], res["boss_rise3b_end"], timedelta(seconds=3600)
        )
    )
    daytime_times = list(
        datetime_range(
            res["daytime_set_start"], res["daytime_set_end"], timedelta(seconds=3600)
        )
    )
    boss_sunset_times = list(
        datetime_range(
            res["boss_sunset_start"], res["boss_sunset_end"], timedelta(seconds=3600)
        )
    )
    boss_set_times = list(
        datetime_range(
            res["boss_set_start"], res["boss_set_end"], timedelta(seconds=3600)
        )
    )

    # fmt: off
    boss_table = boss_night_times + boss_rise3a_times + boss_rise10_times + boss_rise3b_times + boss_sunset_times + boss_set_times + daytime_times
    
    

    boss_table_df = pd.DataFrame({"date_time": boss_table})
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

combined_df = pd.concat(final_result, ignore_index=True)
print(combined_df)


# Create a list of dates between the start and end date
datetime_range(start_date, end_date, timedelta(seconds=3600))
