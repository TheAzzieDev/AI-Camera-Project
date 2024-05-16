from ultralytics import YOLO
import cv2
from datetime import datetime
import os
import uuid
import requests

model = YOLO("models/yolov8n.pt")
temp_id = None
counter = 0
switch = False


def make_file(image):
    date = datetime.now()
    folder_path = f"static/detections/{date.year}-{date.month}-{date.day}"
    if not os.path.exists(folder_path):
        # Create the folder/directory
        os.makedirs(folder_path)
    filename = f"{date.hour}h{date.minute}m{date.second}s_{(uuid.uuid1().hex)[0:10]}.jpg"
    output = os.path.join(os.getcwd(), folder_path, filename)
    print(f"output: {output}")
    cv2.imwrite(output, image)

#Enter the Ip adress for the camera in VideoCapture
def func():
    cap = cv2.VideoCapture("Enter ip to camerahere")
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        framerot = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        result = model.track(framerot, persist=True)
        #xyxy tracker conf clsnummer
        #res_list = result[0].boxes.data
        for box in result[0].boxes:
            print(f"cls: {result[0].names[box.cls[0].item()]} confidence: {float(box.conf[0].item())}")
            print(f"result.boxes: {result[0].boxes}")
            cond = box.cls[0].item() == 0 
            if cond:
                if float(box.conf[0].item()) > 0.5:
                    make_file(framerot)
                    print(f"intruder: {float(box.conf[0].item())}")

        plotted_image = result[0].plot()
        cv2.namedWindow('Video', cv2.WINDOW_KEEPRATIO)
        # width: 1080 height: 1920
        cv2.resizeWindow('Video', int(1080/2), int(1920/2))
        cv2.imshow('Video', plotted_image)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
       
func()
