from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
)
from werkzeug.utils import secure_filename
from skimage.segmentation import slic
from skimage.segmentation import mark_boundaries
from skimage.util import img_as_float
from skimage import io
import json
import matplotlib.pyplot as plt
import argparse
import numpy as np
import cv2
import os
from os.path import getsize


clicked_points = set()
image_base = np.array([[1]])
imgae_work = np.array([[1]])
segments = np.array([[1]])
name = "a"
image_path = "a"
data1 = dict()
jsonimg = np.array([[1]])
basepath = "a"

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        return ("", 204)
    return render_template("slt.html")


@app.route("/drag_draw", methods=["GET", "POST"])
def drag_draw():
    global image_base
    global segments
    global imgae_work
    global jsonimg

    if request.method == "POST":

        h = request.form["selectcolor"].lstrip("#")
        color = tuple(int(h[i : i + 2], 16) for i in (4, 2, 0))
        x_value = int(request.form["x_value"])
        y_value = int(request.form["y_value"])

        clicked_points.add((y_value, x_value))
        for point in clicked_points:
            imgae_work[segments == segments[point[0], point[1]]] = color
            jsonimg[segments == segments[point[0], point[1]]] = (255, 255, 255)

        clicked_points.clear()

        cv2.imwrite(os.path.join(image_path, "a1.jpg"), imgae_work)
        return ("", 204)

    return render_template("slt.html")


@app.route("/drag_erase", methods=["GET", "POST"])
def drag_erase():
    global image_base
    global segments
    global imgae_work
    global jsonimg

    if request.method == "POST":

        x_value = int(request.form["x_value"])
        y_value = int(request.form["y_value"])

        clicked_points.add((y_value, x_value))
        for point in clicked_points:
            imgae_work[segments == segments[point[0], point[1]]] = image_base[
                segments == segments[point[0], point[1]]
            ]
            jsonimg[segments == segments[point[0], point[1]]] = (0, 0, 0)

        clicked_points.clear()
        cv2.imwrite(os.path.join(image_path, "a1.jpg"), imgae_work)
        return ("", 204)
    return render_template("slt.html")


@app.route("/click_draw", methods=["POST"])
def click_draw():
    global image_base
    global segments
    global imgae_work

    data = request.get_json()
    h = data["selectcolor"].lstrip("#")
    color = tuple(int(h[i : i + 2], 16) for i in (4, 2, 0))

    x_value = int(data["x_value"])
    y_value = int(data["y_value"])
    clicked_points.add((y_value, x_value))

    for point in clicked_points:
        imgae_work[segments == segments[point[0], point[1]]] = color
        jsonimg[segments == segments[point[0], point[1]]] = (255, 255, 255)

    clicked_points.clear()
    cv2.imwrite(os.path.join(image_path, "a1.jpg"), imgae_work)

    return {"result": "success", "filename": "a"}


@app.route("/click_erase", methods=["POST"])
def click_erase():
    global image_base
    global segments
    global imgae_work
    global jsonimg

    data = request.get_json()

    x_value = int(data["x_value"])
    y_value = int(data["y_value"])
    clicked_points.add((y_value, x_value))

    for point in clicked_points:
        imgae_work[segments == segments[point[0], point[1]]] = image_base[
            segments == segments[point[0], point[1]]
        ]
        jsonimg[segments == segments[point[0], point[1]]] = (0, 0, 0)

    clicked_points.clear()
    cv2.imwrite(os.path.join(image_path, "a1.jpg"), imgae_work)

    return {"result": "success", "filename": "a"}


@app.route("/get_img", methods=["GET"])
def get_img():
    global name
    return jsonify(img1=name)


@app.route("/segmentation", methods=["GET", "POST"])
def segmentation():
    if request.method == "POST":
        global image_base
        global segments
        global name
        global imgae_work
        global image_path
        global jsonimg
        global basepath

        f = request.files["file_upload"]
        basepath = os.path.dirname(__file__)
        image_path = os.path.join(basepath, "static", "images")
        file_path = os.path.join(
            basepath, "upload", "images", secure_filename(f.filename)
        )
        print(file_path)
        f.save(file_path)

        name = secure_filename(f.filename)

        image_base = cv2.imread(file_path)
        jsonimg = np.zeros((image_base.shape[0], image_base.shape[1], 3), np.uint8)
        imgae_work = image_base.copy()
        numSegments = 1000
        segments = slic(image_base, n_segments=numSegments, sigma=0.1)
        image_slic = mark_boundaries(image_base, segments, color=(0.1, 0.5, 0))
        io.imsave(
            os.path.join(basepath, "static", "images", secure_filename(f.filename)),
            image_slic,
        )
        io.imsave(
            os.path.join(basepath, "static", "images", "a1.jpg"),
            image_base,
        )

        return redirect(
            url_for("predict_scuess", file_name_=secure_filename(f.filename))
        )

    else:
        return render_template("slt.html")


@app.route("/predict_success/<file_name_>", methods=["GET", "POST"])
def predict_scuess(file_name_):
    return render_template("seg.html", image_file="images/" + file_name_)


@app.route("/store_json", methods=["POST", "GET"])
def store_json():
    global name
    global image_path
    global data1
    global jsonimg
    global basepath

    classname = request.form["class"]
    coord_x = []
    coord_y = []

    imgray = cv2.cvtColor(jsonimg, cv2.COLOR_BGR2GRAY)
    ret, imthres = cv2.threshold(imgray, 127, 255, cv2.THRESH_BINARY)
    contour, hierarchy = cv2.findContours(
        imthres, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )

    for i in contour:
        for j in i:
            coord_x.append(int(j[0][0]))
            coord_y.append(int(j[0][1]))

    size = str(getsize(os.path.join(image_path, name)))
    data1 = {
        name
        + size: {
            "fileref": "",
            "size": size,
            "filename": name,
            "base64_img_data": "",
            "file_attributes": {},
            "regions": {
                "0": {
                    "shape_attributes": {
                        "name": "polygon",
                        "all_points_x": coord_x,
                        "all_points_y": coord_y,
                    },
                    "region_attributes": {"class": classname},
                }
            },
        }
    }
    with open(
        os.path.join(basepath, "upload", "jfile", "test.json"), "w", encoding="utf-8"
    ) as make_file:
        json.dump(data1, make_file)
    return ("", 204)


@app.route("/jjjj", methods=["POST", "GET"])
def jjjj():
    global basepath
    with open(os.path.join(basepath, "upload", "jfile", "test.json"), "r") as f:
        json_data = json.load(f)
    return jsonify(result="success", result2=json.dumps(json_data))


if __name__ == "__main__":
    app.run(debug=True)
