import datetime
import pytest
import sys
import io
from src.tests.recording_times_generator_tests import calculate_sun_times, datetime_range, create_date_times_list, assign_time_category, create_random_samples


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
    

# Define test cases
def test_assign_time_category_early_sunrise():
    # Test for the 'EarlySunrise' category
    row = {
        "sunrise": datetime.datetime(2023, 7, 19, 6, 0),
        "sunset": datetime.datetime(2023, 7, 19, 20, 0),
        "NewDate": datetime.datetime(2023, 7, 19, 5, 59, 59),
        "sunrise_next": datetime.datetime(2023, 7, 20, 6, 0),
    }
    assert assign_time_category(row) == "EarlySunrise"

def test_assign_time_category_mid_sunrise():
    # Test for the 'MidSunrise' category
    row = {
        "sunrise": datetime.datetime(2023, 7, 19, 6, 0),
        "sunset": datetime.datetime(2023, 7, 19, 20, 0),
        "NewDate": datetime.datetime(2023, 7, 19, 7, 0),
        "sunrise_next": datetime.datetime(2023, 7, 20, 6, 0),
    }
    assert assign_time_category(row) == "MidSunrise"
    
def test_assign_time_category_late_sunrise():
    # Test for the 'LateSunrise' category
    row = {
        "sunrise": datetime.datetime(2023, 7, 19, 6, 0),
        "sunset": datetime.datetime(2023, 7, 19, 20, 0),
        "NewDate": datetime.datetime(2023, 7, 19, 10, 23),
        "sunrise_next": datetime.datetime(2023, 7, 20, 6, 0),
    }
    assert assign_time_category(row) == "LateSunrise"
    
def test_assign_time_category_daytime():
    # Test for the 'Daytime' category
    row = {
        "sunrise": datetime.datetime(2023, 7, 20, 6, 0),
        "sunset": datetime.datetime(2023, 7, 20, 20, 0),
        "NewDate": datetime.datetime(2023, 7, 20, 13, 30),
        "sunrise_next": datetime.datetime(2023, 7, 21, 6, 0),
    }
    assert assign_time_category(row) == "Daytime"
    
def test_assign_time_category_dusk():
    # Test for the 'Dusk' category
    row = {
        "sunrise": datetime.datetime(2023, 7, 20, 6, 0),
        "sunset": datetime.datetime(2023, 7, 20, 20, 0),
        "NewDate": datetime.datetime(2023, 7, 20, 20, 57),
        "sunrise_next": datetime.datetime(2023, 7, 21, 6, 0),
    }
    assert assign_time_category(row) == "Dusk"

def test_assign_time_category_nocturnal():
    # Test for the 'Dusk' category
    row = {
        "sunrise": datetime.datetime(2023, 7, 22, 6, 0),
        "sunset": datetime.datetime(2023, 7, 22, 20, 0),
        "NewDate": datetime.datetime(2023, 7, 20, 1, 28),
        "sunrise_next": datetime.datetime(2023, 7, 23, 6, 0),
    }
    assert assign_time_category(row) == "Nocturnal"
    
# Define test cases
def test_create_random_samples_no_sample_size():
    # Test when sample_size is None
    combined_timings = [
        {"category": "EarlySunrise", "data": "sample1", "sunrise_next": datetime.datetime(2023, 7, 23, 6, 0), "NewDate": datetime.datetime(2023, 7, 20, 1, 28)},
        {"category": "EarlySunrise", "data": "sample2", "sunrise_next": datetime.datetime(2023, 7, 23, 6, 0), "NewDate": datetime.datetime(2023, 7, 20, 1, 28)},
        {"category": "MidSunrise", "data": "sample3", "sunrise_next": datetime.datetime(2023, 7, 23, 6, 0), "NewDate": datetime.datetime(2023, 7, 20, 1, 28)},
    ]
    sample_size = None
    result = create_random_samples(combined_timings, sample_size)
    assert len(result) == 3
    
def test_create_random_samples_valid_sample_size():
    # Test when sample_size is valid for all categories
    combined_timings = [
        {"category": "EarlySunrise", "data": "sample1", "sunrise_next": datetime.datetime(2023, 7, 23, 6, 0), "NewDate": datetime.datetime(2023, 7, 20, 1, 28)},
        {"category": "EarlySunrise", "data": "sample2", "sunrise_next": datetime.datetime(2023, 7, 23, 6, 0), "NewDate": datetime.datetime(2023, 7, 20, 1, 28)},
        {"category": "MidSunrise", "data": "sample3", "sunrise_next": datetime.datetime(2023, 7, 23, 6, 0), "NewDate": datetime.datetime(2023, 7, 20, 1, 28)},
        {"category": "MidSunrise", "data": "sample4", "sunrise_next": datetime.datetime(2023, 7, 23, 6, 0), "NewDate": datetime.datetime(2023, 7, 20, 1, 28)},
        {"category": "LateSunrise", "data": "sample5", "sunrise_next": datetime.datetime(2023, 7, 23, 6, 0), "NewDate": datetime.datetime(2023, 7, 20, 1, 28)},
        {"category": "LateSunrise", "data": "sample6", "sunrise_next": datetime.datetime(2023, 7, 23, 6, 0), "NewDate": datetime.datetime(2023, 7, 20, 1, 28)},
        {"category": "Daytime", "data": "sample7", "sunrise_next": datetime.datetime(2023, 7, 23, 6, 0), "NewDate": datetime.datetime(2023, 7, 20, 1, 28)},
        {"category": "Daytime", "data": "sample8", "sunrise_next": datetime.datetime(2023, 7, 23, 6, 0), "NewDate": datetime.datetime(2023, 7, 20, 1, 28)},
        {"category": "Dusk", "data": "sample9", "sunrise_next": datetime.datetime(2023, 7, 23, 6, 0), "NewDate": datetime.datetime(2023, 7, 20, 1, 28)},
        {"category": "Dusk", "data": "sample10", "sunrise_next": datetime.datetime(2023, 7, 23, 6, 0), "NewDate": datetime.datetime(2023, 7, 20, 1, 28)},
        {"category": "Nocturnal", "data": "sample11", "sunrise_next": datetime.datetime(2023, 7, 23, 6, 0), "NewDate": datetime.datetime(2023, 7, 20, 1, 28)},
        {"category": "Nocturnal", "data": "sample12", "sunrise_next": datetime.datetime(2023, 7, 23, 6, 0), "NewDate": datetime.datetime(2023, 7, 20, 1, 28)},
    ]
    sample_size = 2
    result = create_random_samples(combined_timings, sample_size)
    assert len(result) == 12  # 2 samples from each category
    

def test_create_random_samples_invalid_sample_size():
    # Test when sample_size is greater than the number of samples in a category
    combined_timings = [
        {"category": "EarlySunrise", "data": "sample1", "sunrise_next": datetime.datetime(2023, 7, 23, 6, 0), "NewDate": datetime.datetime(2023, 7, 20, 1, 28)},
        {"category": "EarlySunrise", "data": "sample2", "sunrise_next": datetime.datetime(2023, 7, 23, 6, 0), "NewDate": datetime.datetime(2023, 7, 20, 1, 28)},
        {"category": "MidSunrise", "data": "sample3", "sunrise_next": datetime.datetime(2023, 7, 23, 6, 0), "NewDate": datetime.datetime(2023, 7, 20, 1, 28)},
    ]
    sample_size = 5
    
    
    # Calling the function
    create_random_samples(combined_timings, sample_size)
    
    assert "Please have smaller sample size for the desired dates mentioned."
