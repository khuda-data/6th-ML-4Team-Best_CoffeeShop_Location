kapt도로명주소from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import pandas as pd
import time
from collections import defaultdict

# Load the data from the CSV file
file_path = 'C:\Users\pjung\OneDrive\문서\정현\동아리\쿠다\TP\2023상권유동인구.csv'
data = pd.read_csv(file_path)

# Initialize Nominatim API
geolocator = Nominatim(user_agent="South Korea")

def get_lat_lon(district_name, retries=3, delay=1):
    """
    Returns the latitude and longitude for a given commercial district name with retry logic.
    
    Parameters:
    district_name (str): The name of the commercial district.
    retries (int): Number of times to retry in case of a timeout.
    delay (float): Delay in seconds between retries.
    
    Returns:
    tuple: A tuple containing latitude and longitude.
    """
    try:
        location = geolocator.geocode(district_name)
        if location:
            return (location.latitude, location.longitude)
        else:
            return (None, None)
    except GeocoderTimedOut:
        if retries > 0:
            time.sleep(delay)
            return get_lat_lon(district_name, retries=retries-1, delay=delay * 2)  # Exponential backoff
        else:
            return (None, None)

# Cache to store previously fetched latitudes and longitudes
coordinates_cache = defaultdict(lambda: (None, None))

# Initialize empty lists to store latitude and longitude
latitudes = []
longitudes = []

# Iterate over each district name in the DataFrame
for district_name in data['kapt도로명주소']:
    if district_name in coordinates_cache:
        lat, lon = coordinates_cache[district_name]
    else:
        lat, lon = get_lat_lon(district_name)
        coordinates_cache[district_name] = (lat, lon)
    
    latitudes.append(lat)
    longitudes.append(lon)
    time.sleep(1)  # Sleep to prevent overwhelming the geocoding service

# Add the new latitude and longitude columns to the DataFrame
data['Latitude'] = latitudes
data['Longitude'] = longitudes

# Save the updated DataFrame to a new CSV file
data.to_csv('C:/Users/pjung/OneDrive/문서/정현/동아리/쿠다/TP/서울시아파트_with_coordinates.csv', index=False)

print("Updated DataFrame with latitude and longitude saved as '서울시아파트_with_coordinates.csv'.")
