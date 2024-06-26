# **🚧 Pothole Patrol: Smart Detection & Reporting System 🚗**

## Overview
Pothole Patrol is your vigilant ally in the battle against road hazards. Leveraging the cutting-edge technology of OAK-D (OpenCV AI Kit with Depth), Raspberry Pi, and the prowess of YOLO (You Only Look Once) object detection, this project brings forth a revolution in road safety and infrastructure maintenance.

## Features 🛠️
* Automated Detection: Seamlessly identify potholes in real-time with the power of computer vision.
* Effortless Reporting: Instantly upload detected potholes to Google Drive, streamlining data collection and analysis.
* Precision Localization: Pinpoint the exact GPS coordinates of potholes for efficient repair and maintenance efforts.
* Modular Design: Built upon depthai-experiments repo for detection and integrated with a GPS module for accurate location tracking.

## How It Works 🤖
Pothole Detection operates with remarkable efficiency:

* Detection: OAK-D scans the road, identifying potholes with precision.
* Localization: Simultaneously, the GPS module records the location of each detected pothole.
* Reporting: Detected potholes are automatically uploaded to Google Drive, providing crucial data for road maintenance authorities.

## Installation & Setup 🚀
1. Connect the OAK D to Rpi.

   
### Google Drive setup

Follow the instructions :
> *[Google Drive API Setup](https://developers.google.com/drive/api/quickstart/python#objectives)*.

> Go to Cloud console -> APIs & Services -> Credentials.

> Download the .json file and rename it as **credentials.json** and save it in the same directory as upload.py.

> Run the upload.py script and authorize to get token.json.

> All set with Google Drive API!

### GPS setup
* Power the module and it will automatically acquire satellite signals and a position fix. Once it has a position fix the module will blink the on board LED. This LED will continue to blink while the module has a position fix.
  
1. Hardware Part:
   > Connect the pins, accordingly
      Neo 6M VCC -----> Raspberry pi 5v
		Neo 6M GND -----> Raspberry pi GND
		Neo 6M  RX -----> Raspberry pi TX (gpio 14) 
		Neo 6M  TX -----> Raspberry pi RX (gpio 15)
  
3. Software Part:
   > First we need to edit the /boot/config.txt file.
      * At the end of the file add the following lines:
         dtparam=spi=on
         dtoverlay=pi3-disable-bt
         core_freq=250
         enable_uart=1
         force_turbo=1
   	* Now save this by typing ctrl +x, then type y and press enter.
   > Reboot the system.
   > When the blue led is blinking, run the following command:
      sudo cat /dev/ttyAMA0
   
   > Run gps_print.py file

## Usage 📝

Turn on the Rpi with OAK-D and GPS connectivity.

1. Clone the Repository:
   
   > git clone https://github.com/AmitHegde3/Pothole_Detection_DL_IOT

2. Install Dependencies:

   > cd Pothole_Detection_DL_IOT
   
   > pip install -r requirements.txt

3. Run the main_api.py Script

   > python3 main_api.py -m (.blob file path) -c (.json file path) 

(By default Pre Trained YoloV7 model will run. Just Type: **python3 main_api.py** )

## License 📄

This project is licensed under the MIT License.

## Contact 📧
For inquiries and support, please contact *[Amit Hegde](hegdeamit6@gmail.com)*.
