from geopy.geocoders import Nominatim

def get_address(latitude, longitude):
    # Create a geolocator object using Nominatim
    geolocator = Nominatim(user_agent="my_geocoder")

    # Concatenate the latitude and longitude into a single string
    location = f"{latitude}, {longitude}"

    try:
        # Use geocode to get the location information
        location_info = geolocator.reverse(location, language='en')
        
        # Extract and print the address
        address = location_info.address
        print(f"Address: {address}")

    except Exception as e:
        print(f"Error: {str(e)}")

# Example usage:
latitude = 12.9410  # Replace with your desired latitude
longitude = 77.5655  # Replace with your desired longitude

get_address(latitude, longitude)

