from depthai_sdk import OakCamera
from gps_print import get_current_location
from upload import main

from PIL import ImageGrab
import cv2
import numpy as np
import os

def get_info(packet):
    #print(f'Number of objects detected: {len(packet.detections)}')
    if(packet.detections):
        li = []
        for t in packet.detections:
            li.append(t.confidence)
        
        if(max(li) > 0.97):
             print(f"Confidence is: {max(li)}")
             image = ImageGrab.grab()
             print("Screenshot captured!")
             image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
             address = get_current_location()
             print("Address fetched!")
             cv2.putText(image, address, (10,60), cv2.FONT_HERSHEY_SIMPLEX,0.7, (0, 0, 255),2)
             cv2.imwrite("annotated_image.jpg", image)
             print("Image saved!")
             main()
             
             #os._exit(1)
             
             
with OakCamera() as oak:
    
    color = oak.create_camera('color')
    nn = oak.create_nn('best.json', color, nn_type='yolo', spatial=None,decode_fn=None)
    
    visualizer = oak.visualize(nn,fps=True, scale=1.5)
    
    oak.callback(nn, callback=get_info)
    
    oak.start(blocking=True)
    
    
