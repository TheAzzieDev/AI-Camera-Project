from flask import *
from flask_cors import CORS
import cv2
import numpy as np
from ultralytics import YOLO
from datetime import datetime
import os
import uuid
import glob
import tracking
app = Flask(__name__)
CORS(app)



@app.route("/", methods = ["GET"])
def index():
    return render_template("index.html")

@app.route("/panel", methods = ["GET"])
def panel():
    path = r'static/detections/**/*.jpg'

    image_list = glob.glob(path, recursive = True)

    file_info = []
    dir_set = set()


    for image_path in image_list:
        start = image_path.find("static")
        end = start + 7
        path_name = image_path[end:]

        file_info.append((path_name.replace("\\", "/"), os.path.basename(image_path)))
        dirname = os.path.basename(os.path.dirname(image_path))    
        dir_set.add(dirname)
   
    return render_template("panel.html", directories=dir_set, file_info=file_info)
    

if __name__ == "__main__":
    app.run(debug=True, host = "0.0.0.0", port=8080)