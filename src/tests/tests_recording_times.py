import datetime
import pytest
from src.tests.recording_times_generator_tests import calculate_sun_times, datetime_range, create_date_times_list


def test_calculate_sun_times():
    # Test case 1: Verify the output for a specific date, latitude, and longitude
    date = datetime.date(2023, 7, 19)
    latitude = 37.7749  # Replace with your latitude
    longitude = -122.4194  # Replace with your longitude

    result = calculate_sun_times(date, latitude, longitude)


    assert isinstance(result, dict)
    
    assert "nocturnal_start_time" in result
    assert "nocturnal_end_time" in result
    assert "sunrise_start_time" in result
    assert "sunrise_end_time" in result
    assert "daytime_start_time" in result
    assert "daytime_end_time" in result
    assert "dusk_start_time" in result
    assert "dusk_end_time" in result
    
    
    # Test case 2: Verify the output for another date, latitude, and longitude
    date = datetime.date(2023, 8, 21)
    latitude = 40.7128  # Replace with your latitude
    longitude = -74.0060  # Replace with your longitude

    result = calculate_sun_times(date, latitude, longitude)

    assert isinstance(result, dict)
    
    assert "nocturnal_start_time" in result
    assert "nocturnal_end_time" in result
    assert "sunrise_start_time" in result
    assert "sunrise_end_time" in result
    assert "daytime_start_time" in result
    assert "daytime_end_time" in result
    assert "dusk_start_time" in result
    assert "dusk_end_time" in result
    
    
    # Test case 3: Verify the output for an invalid date
    date = datetime.date(2023,7,19)  # Invalid date format, should raise an exception

    if not isinstance(date, datetime.date):
        raise TypeError("Invalid date format. Please use datetime.date(YYYY-MM-DD)")
    


@pytest.mark.parametrize(
    "start, end, delta, expected",
    [
        (
            datetime.datetime(2022, 1, 1),
            datetime.datetime(2022, 1, 1),
            datetime.timedelta(minutes=30),
            [datetime.datetime(2022, 1, 1)],
        ),
        (
            datetime.datetime(2022, 1, 1),
            datetime.datetime(2022, 1, 1, 1, 30),
            datetime.timedelta(minutes=30),
            [
                datetime.datetime(2022, 1, 1, 0, 0),
                datetime.datetime(2022, 1, 1, 0, 30),
                datetime.datetime(2022, 1, 1, 1, 0),
                datetime.datetime(2022, 1, 1, 1, 30),
            ],
        ),
    ],
)
def test_datetime_range(start, end, delta, expected):
    assert list(datetime_range(start, end, delta)) == expected
    
    

# Test create_date_times_list function
@pytest.mark.parametrize(
    "date_range, result, user_start_date, user_end_date, expected_len",
    [
        # Define test cases here based on the input and expected output
        # Example:
        (
            # date_range: A list of datetime objects
            # result: A list of dictionaries with time ranges
            # user_start_date: datetime object representing user-defined start date
            # user_end_date: datetime object representing user-defined end date
            # expected_len: Expected length of the final_result list
            [datetime.datetime(2022, 1, 1)],
            [
                {
                    "nocturnal_start_time": datetime.datetime(2022, 1, 1, 22, 0),
                    "nocturnal_end_time": datetime.datetime(2022, 1, 2, 4, 0),
                    "sunrise_start_time": datetime.datetime(2022, 1, 2, 6, 30),
                    "sunrise_end_time": datetime.datetime(2022, 1, 2, 7, 0),
                    "daytime_start_time": datetime.datetime(2022, 1, 2, 8, 0),
                    "daytime_end_time": datetime.datetime(2022, 1, 2, 17, 0),
                    "dusk_start_time": datetime.datetime(2022, 1, 2, 18, 30),
                    "dusk_end_time": datetime.datetime(2022, 1, 2, 19, 0),
                    "sunrise": "6:30 AM",
                    "sunset": "5:00 PM",
                    "sunrise_next": "6:30 AM",
                }
            ],
            datetime.datetime(2022, 1, 1),
            datetime.datetime(2022, 1, 2),
            5,  # Expected length of the final_result list for this case. 5 different values of datetime objects
        ),
      
    ],
)
def test_create_date_times_list(date_range, result, user_start_date, user_end_date, expected_len):
    final_result = create_date_times_list(date_range, result, user_start_date, user_end_date)
    assert len(final_result) == expected_len