#!/usr/bin/env python3
"""
The code is edited from docs (https://docs.luxonis.com/projects/api/en/latest/samples/Yolo/tiny_yolo/)
We add parsing from JSON files that contain configuration
"""

from pathlib import Path
import sys
sys.path.append("/home/frps/.local/lib/python3.11/site-packages")
import cv2
import depthai as dai
import numpy as np
import time
import argparse
import json
import blobconverter
import os
import datetime

from gps_print import get_current_location
from upload import main
from buzzer_sound import buzz
from LED import ledStart,ledBlink,ledBlue

save_dir = 'detected_images'
os.makedirs(save_dir,exist_ok=True)
frame_count = 0

# parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("-m", "--model", help="Provide model name or model path for inference",
                    default='/home/frps/Desktop/Pothole/Trained Models/Yolov7_Seniors/best_openvino_2022.1_6shave.blob', type=str)
parser.add_argument("-c", "--config", help="Provide config path for inference",
                    default='/home/frps/Desktop/Pothole/Trained Models/Yolov7_Seniors/best.json', type=str)
                    #Relative path: ./Trained Models/Yolov7_Seniors/best.json
                    #Relative blob path : ./Trained Models/Yolov7_Seniors/best_openvino_2022.1_6shave.blob
                    #/home/frps/Desktop/Pothole/Trained Models/Yolov7_Seniors/best_openvino_2022.1_6shave.blob
                    #/home/frps/Desktop/Pothole/Trained Models/Yolov7_Seniors/best.json
                    
args = parser.parse_args()

# parse config
configPath = Path(args.config)
if not configPath.exists():
    raise ValueError("Path {} does not exist!".format(configPath))

with configPath.open() as f:
    config = json.load(f)
nnConfig = config.get("nn_config", {})

# parse input shape
if "input_size" in nnConfig:
    W, H = tuple(map(int, nnConfig.get("input_size").split('x')))

# extract metadata
metadata = nnConfig.get("NN_specific_metadata", {})
classes = metadata.get("classes", {})
coordinates = metadata.get("coordinates", {})
anchors = metadata.get("anchors", {})
anchorMasks = metadata.get("anchor_masks", {})
iouThreshold = metadata.get("iou_threshold", {})
confidenceThreshold = metadata.get("confidence_threshold", {})

print(metadata)

# parse labels
nnMappings = config.get("mappings", {})
labels = nnMappings.get("labels", {})

# get model path
nnPath = args.model
if not Path(nnPath).exists():
    print("No blob found at {}. Looking into DepthAI model zoo.".format(nnPath))
    nnPath = str(blobconverter.from_zoo(args.model, shaves = 6, zoo_type = "depthai", use_cache=True))
# sync outputs
syncNN = True

# Create pipeline
pipeline = dai.Pipeline()

# Define sources and outputs
camRgb = pipeline.create(dai.node.ColorCamera)
detectionNetwork = pipeline.create(dai.node.YoloDetectionNetwork)
xoutRgb = pipeline.create(dai.node.XLinkOut)
nnOut = pipeline.create(dai.node.XLinkOut)

xoutRgb.setStreamName("rgb")
nnOut.setStreamName("nn")

# Properties
camRgb.setPreviewSize(W, H)

camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
camRgb.setInterleaved(False)
camRgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.BGR)
camRgb.setFps(60)

# Network specific settings
detectionNetwork.setConfidenceThreshold(confidenceThreshold)
detectionNetwork.setNumClasses(classes)
detectionNetwork.setCoordinateSize(coordinates)
detectionNetwork.setAnchors(anchors)
detectionNetwork.setAnchorMasks(anchorMasks)
detectionNetwork.setIouThreshold(iouThreshold)
detectionNetwork.setBlobPath(nnPath)
detectionNetwork.setNumInferenceThreads(2)
detectionNetwork.input.setBlocking(False)

# Linking
camRgb.preview.link(detectionNetwork.input)
detectionNetwork.passthrough.link(xoutRgb.input)
detectionNetwork.out.link(nnOut.input)

#buzz(2)
ledBlue()
ledStart()


# Connect to device and start pipeline
with dai.Device(pipeline) as device:

    # Output queues will be used to get the rgb frames and nn data from the outputs defined above
    qRgb = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)
    qDet = device.getOutputQueue(name="nn", maxSize=4, blocking=False)

    frame = None
    detections = []
    startTime = time.monotonic()
    counter = 0
    color2 = (255, 255, 255)

    # nn data, being the bounding box locations, are in <0..1> range - they need to be normalized with frame width/height
    def frameNorm(frame, bbox):
        normVals = np.full(len(bbox), frame.shape[0])
        normVals[::2] = frame.shape[1]
        return (np.clip(np.array(bbox), 0, 1) * normVals).astype(int)

    def displayFrame(name, frame, detections):
        ledBlink()
        color = (255, 0, 0)
        #li = []
        for detection in detections:
            bbox = frameNorm(frame, (detection.xmin, detection.ymin, detection.xmax, detection.ymax))
            cv2.putText(frame, labels[detection.label], (bbox[0] + 10, bbox[1] + 20), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
            cv2.putText(frame, f"{int(detection.confidence * 100)}%", (bbox[0] + 10, bbox[1] + 40), cv2.FONT_HERSHEY_TRIPLEX, 0.5,(0,0, 255))
            cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, 2)
            #li.append(detection.confidence * 100)
        # Show the frame-----------------------------------------------------------------------------
            if(detection.confidence>0.93):
                
                #buzz(2)
                #ledStart()
                ledBlue()
                print(detection.confidence*100)
                address = get_current_location()
                print("Address fetched!")
                cv2.putText(frame, address, (10,60), cv2.FONT_HERSHEY_SIMPLEX,0.7, (0, 0, 255),2)
                cv2.imwrite("annotated_image.jpg", frame)
                current_time = datetime.datetime.now()
                image_name = current_time.strftime("detetced_iamge_%Y-%m-%d_%H-%M-%S.jpg")
                cv2.imwrite(os.path.join(save_dir,image_name),frame)
                #main()
                print("Image Saved in Cloud")
                #buzz(3)
                ledBlue()
            
        #cv2.imshow(name,frame)



    while True:
        inRgb = qRgb.get()
        inDet = qDet.get()

        if inRgb is not None:
            frame = inRgb.getCvFrame()
            cv2.putText(frame, "NN fps: {:.2f}".format(counter / (time.monotonic() - startTime)),
                        (2, frame.shape[0] - 4), cv2.FONT_HERSHEY_TRIPLEX, 0.4, color2)

        if inDet is not None:
            detections = inDet.detections
            counter += 1

        if frame is not None:
            displayFrame("Pothole Detection", frame, detections)

        #if cv2.waitKey(1) == ord('q'):
          #  break
