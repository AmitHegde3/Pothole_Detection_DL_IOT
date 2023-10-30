import serial
import pynmea2
from geopy.geocoders import Nominatim

def get_address(lat,lng):
    # Create a geolocator object using Nominatim
    geolocator = Nominatim(user_agent="my_geocoder")

    # Concatenate the latitude and longitude into a single string
    location = f"{lat}, {lng}"

    try:
        # Use geocode to get the location information
        location_info = geolocator.reverse(location, language='en')
        
        # Extract and print the address
        address = location_info.address
        print(f"Address: {address}")

    except Exception as e:
        print(f"Error: {str(e)}")

while True:
        port="/dev/ttyAMA0"
        ser=serial.Serial(port, baudrate=9600, timeout=0.5)
        dataout = pynmea2.NMEAStreamReader()
        newdata=ser.readline()
        n_data = newdata.decode('latin-1')
        if n_data[0:6] == '$GPRMC':
                newmsg=pynmea2.parse(n_data)
                lat=newmsg.latitude
                lng=newmsg.longitude
                gps = "Latitude=" + str(lat) + " and Longitude=" + str(lng)
                print(gps)
                get_address(lat,lng)
                
                


