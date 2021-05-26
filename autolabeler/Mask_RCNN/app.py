# from __future__ import division, print_function

# coding=utf-8
import sys
import os
import glob
import re
import numpy as np


# from flask_ngrok import run_with_ngrok

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer


from flask import Flask, request, redirect, url_for, flash, jsonify  #
import numpy as np  #
import pickle as p  #
import json  #


import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

import json
import datetime
import skimage.draw
import skimage

# Root directory of the project - MASK_RCNN 폴더가 있는 경로
ROOT_DIR = os.path.abspath("C:\\Mask_RCNN")

# Import Mask RCNN
sys.path.append(ROOT_DIR)  # To find local version of the library
from mrcnn.config import Config
from mrcnn import model as modellib, utils
from mrcnn import visualize

class SurgeryConfig(Config):
    """Configuration for training on the toy  dataset.
    Derives from the base Config class and overrides some values.
    """
    # Give the configuration a recognizable name
    NAME = "surgery"

    # We use a GPU with 12GB memory, which can fit two images.
    # Adjust down if you use a smaller GPU.
    IMAGES_PER_GPU = 2

    # Number of classes (including background)
    NUM_CLASSES = 1 + 2  # Background + balloon

    # Number of training steps per epoch
    STEPS_PER_EPOCH = 100

    # Skip detections with < 90% confidence
    DETECTION_MIN_CONFIDENCE = 0.9


class InferenceConfig(SurgeryConfig):
  GPU_COUNT = 1
  IMAGES_PER_GPU = 1

config = InferenceConfig()
config.display()

#model_dir - Mask_RCNN폴더에 logs 폴더 경로
model = modellib.MaskRCNN(mode="inference", config=config, model_dir='C:\\Mask_RCNN\\logs') 

#weights_path - Mask_RCNN폴더에 weight의 경로
weights_path = 'C:\\Mask_RCNN\\logs\\mask_rcnn_object_0010.h5'

model.load_weights(weights_path, by_name=True)
model.keras_model._make_predict_function()
class_names = ['BG', 'head', 'heart']

TEMPLATE_FOLDER = 'C:\\Mask_RCNN\\templates' # Mask_RCNN폴더에 있는 templates 경로
STATIC_FOLDER = 'C:\\Mask_RCNN\\static' # Mask_RCNN폴더에 있는 static 경로
app = Flask(__name__, template_folder=TEMPLATE_FOLDER, static_folder = STATIC_FOLDER)
# run_with_ngrok(app)  



@app.route("/", methods=["GET"])
def index():
    # Main page
    return render_template("index.html")


@app.route("/predict", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
      f = request.files['file']
      basepath = os.path.dirname(__file__)
      file_path = os.path.join(basepath, "upload",'images', secure_filename(f.filename))
      file_name = secure_filename(f.filename)
      print(file_path)
      f.save(file_path)

      image = skimage.io.imread(file_path)
        
      r = model.detect([image], verbose=1)[0]
      visualize.display_instances(image, r['rois'], r['masks'], r['class_ids'], class_names, r['scores'],image_name=secure_filename(f.filename))
      
      return redirect(url_for('predict_scuess', file_name_ = file_name))
    else:
      return render_template("index.html")


@app.route("/predict_success/<file_name_>", methods=["GET", "POST"])
def predict_scuess(file_name_):
      return render_template('update_index.html',image_file = 'images/'+file_name_)
      
if __name__ == "__main__":
    # modelfile = "/content/drive/MyDrive/Colab Notebooks/MasRcnn-WebApp-master/model.py"
    # model = open(modelfile, "rb")  #
    app.run() 

