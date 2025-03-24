from ultralytics import YOLO
import cv2
from datetime import datetime
import os
import uuid


def make_file(image):

    date = datetime.now()

    folder_path = f"static\\detections\\{date.year}-{date.month}-{date.day}"

    if not os.path.exists(folder_path):

        os.makedirs(folder_path)

    filename = f"{date.hour}h{date.minute}m{date.second}s_{(uuid.uuid1().hex)[0:10]}.jpg"

    output = os.path.join(os.getcwd(), folder_path, filename)

    cv2.imwrite(output, image)


#Enter the Ip adress for the camera in VideoCapture
def capture_images():

    cap = cv2.VideoCapture(0)

    model = YOLO("models/yolov8n.pt")

    time_in_seconds = 0

    time_in_seconds_before = 0


    while cap.isOpened():

        ret, frame = cap.read()

        if not ret:
            break
        
        result = model.track(frame, persist=True)
        time_in_seconds = int(datetime.now().strftime("%S"))

        time_difference = abs(time_in_seconds - time_in_seconds_before)
        plotted_image = result[0].plot()

        for box in result[0].boxes:


            cond = box.cls[0].item() == 0 

            if cond:
                if float(box.conf[0].item()) > 0.5 and time_difference >= 3:

                    make_file(plotted_image)

                    print(f"intruder: {float(box.conf[0].item())}")
                    time_in_seconds_before = time_in_seconds

        
        cv2.namedWindow('Video', cv2.WINDOW_KEEPRATIO)

        # width: 1080 height: 1920
        cv2.resizeWindow('Video', int(1920/2), int(1080/2),)

        cv2.imshow('Video', plotted_image)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break


def capture_and_send():

    cap = cv2.VideoCapture(0)

    model = YOLO("models/yolov8n.pt")

    time_in_seconds = 0

    time_in_seconds_before = 0


    while cap.isOpened():

        ret, frame = cap.read()

        if not ret:
            break
        
        result = model.track(frame, persist=True)
        time_in_seconds = int(datetime.now().strftime("%S"))

        time_difference = abs(time_in_seconds - time_in_seconds_before)
        plotted_image = result[0].plot()

        for box in result[0].boxes:


            cond = box.cls[0].item() == 0 

            if cond:
                if float(box.conf[0].item()) > 0.5 and time_difference >= 3:

                    make_file(plotted_image)

                    print(f"intruder: {float(box.conf[0].item())}")
                    time_in_seconds_before = time_in_seconds

        
        ret, buffer = cv2.imencode(".jpg", plotted_image)
        plotted_image = buffer.tobytes()
        yield(b'--frame\n' + b'Content-Type: image/jpeg\n\n' + plotted_image + b'\n')


        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

if __name__ == "__main__":  

    capture_images()
