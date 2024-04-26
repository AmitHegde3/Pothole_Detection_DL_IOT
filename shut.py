import os

def shutdown_pi():
	print("Shut Down Initiated")
	os.system("sudo shutdown -h now")

# Call the function to shutdown the Raspberry Pi
#shutdown_pi()
