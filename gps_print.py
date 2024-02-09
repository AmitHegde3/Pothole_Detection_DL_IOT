#!/usr/bin/env python3

import serial
import pynmea2
from geopy.geocoders import Nominatim

def get_current_location():
    def get_address(lat, lng):
        # Create a geolocator object using Nominatim
        geolocator = Nominatim(user_agent="my_geocoder")

        # Concatenate the latitude and longitude into a single string
        location = f"{lat}, {lng}"

        try:
            # Use geocode to get the location information
            location_info = geolocator.reverse(location, language='en')

            # Extract and return the address
            address = location_info.address
            return address

        except Exception as e:
            return str(e)

    port = "/dev/ttyAMA0"
    ser = serial.Serial(port, baudrate=9600, timeout=0.5)
    dataout = pynmea2.NMEAStreamReader()

    while True:
        newdata = ser.readline()
        n_data = newdata.decode('latin-1')
        if n_data[0:6] == '$GPRMC':
            newmsg = pynmea2.parse(n_data)
            lat = newmsg.latitude
            lng = newmsg.longitude
            gps = "Latitude=" + str(lat) + " and Longitude=" + str(lng)
            print(gps)
            address = get_address(lat, lng)
            return address  # Return the address and exit the loop

    # Close the serial port when done
    ser.close()

if __name__ == "__main__":
    address = get_current_location()
    print(f"Current Address: {address}")

