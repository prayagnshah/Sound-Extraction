import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from suncalc import get_times

start_date = pd.to_datetime("2021-07-05", utc=True)
end_date = pd.to_datetime("2021-07-31", utc=True)

# coords = pd.read_csv("GPS_log.csv", skiprows=1)
latitude = 44.72
longitude = -62.80

# run loop
result = []
date_range = pd.date_range(start_date, end_date, freq="D", tz="UTC")


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

print(result)

# result_df = pd.DataFrame(result)

# print(result_df)
