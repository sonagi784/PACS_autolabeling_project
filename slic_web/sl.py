from flask import Flask ,render_template, request, jsonify
from skimage.segmentation import slic
from skimage.segmentation import mark_boundaries
from skimage.util import img_as_float
from skimage import io
import json
import matplotlib.pyplot as plt
import argparse
import numpy as np
import cv2

clicked_points = set()
clone = None
global image1

image = cv2.imread('C:\\sample2.jpg')
clone = image.copy()
numSegments = 1000
segments = slic(image, n_segments = numSegments, sigma = 0.1)
color = (255,0,0)
image1 = clone.copy()
image2 = mark_boundaries(image, segments, color=(0.1,0.5,0))
io.imsave('C:\\software_engin\\static\\images\\labelimage22.jpg', image2)    

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        h=request.form['selectcolor'].lstrip('#')
        color = tuple(int(h[i:i+2], 16) for i in (4, 2, 0))
        print(color)
        x_value = int(request.form['x_value'])
        y_value = int(request.form['y_value'])
        print(x_value, y_value)
        clicked_points.add((y_value,x_value))
        for point in clicked_points:
            image1[segments	== segments[point[0], point[1]]] = color
        clicked_points.clear()
        # cv2.imshow("image123",image1)
        cv2.imwrite('C:\\software_engin\\static\\images\\labelimage1.jpg', image1)
        cv2.imwrite('C:\\imagestore\\labelimage11.jpg', image1)
        return ('', 204)


    return render_template('slt.html',image_file = "static\\images\\labelimage22.jpg", image_file2 = 'static\\images\\labelimage1.jpg')
    
@app.route('/ajax', methods=['POST'])
def ajax():
    data = request.get_json()
    h=data['selectcolor'].lstrip('#')
    color = tuple(int(h[i:i+2], 16) for i in (4, 2, 0))
    print(color)
    x_value = int(data['x_value'])
    y_value = int(data['y_value'])
    print(x_value, y_value)
    clicked_points.add((y_value,x_value))
    for point in clicked_points:
        image1[segments	== segments[point[0], point[1]]] = color
    clicked_points.clear()
    cv2.imwrite('C:\\software_engin\\static\\images\\labelimage1.jpg', image1)
    cv2.imwrite('C:\\imagestore\\labelimage11.jpg', image1)
    data['ur'] = 'static\\images\\labelimage1.jpg'
    print(data)

    return jsonify(result = "success", result2= data)

@app.route('/get_img',methods=['GET'])
def get_img():
    img = 'static\\images\\labelimage1.jpg'
    return jsonify(img1 = img)

@app.route('/submit_img',methods=['POST'])
def submit_img():
    data1 = request.get_json()
    print(data1['path'])
    pathimage = cv2.imread(data1['path'])
    numSegments = 5000
    segments = slic(pathimage, n_segments = numSegments, sigma = 0.1)
    io.imsave('C:\\software_engin\\static\\images\\labelimage33.jpg', mark_boundaries(pathimage, segments, color=(0.1,0.5,0))) 
    return jsonify(result = "success", result2= data1)



    # def MouseLeftClick(event,x,y,flags,param):
    #     if event == cv2.EVENT_LBUTTONDOWN or flags == cv2.EVENT_FLAG_LBUTTON :
    #         clicked_points.add((y,x))
    #         print(y,x)
    #         for point in clicked_points:
    #             image1[segments	== segments[point[0], point[1]]] = color
    #         cv2.imshow("image123",image1)
    #         clicked_points.clear()
    #     elif event == cv2.EVENT_RBUTTONDOWN :
    #         cv2.imwrite('C:\\imagestore\\image123ee.jpg', image1)    
        
    # cv2.imshow("Aaa",mark_boundaries(image, segments, color=(0.1,0.5,0)))
    # cv2.setMouseCallback("Aaa", MouseLeftClick)

    # while True:
    #     key = cv2.waitKey(0)
        
    #     if key==27:
    #         print('key : ',key)
    #         break
    #     elif key == 113 :
    #         color = (100,255,0)
    #         print('key : ',key)
    # cv2.destroyAllWindows()

if __name__ =='__main__':
    app.run(debug =True)


# def MouseLeftClick(event,x,y,flags,param):
#     if event == cv2.EVENT_LBUTTONDOWN or flags == cv2.EVENT_FLAG_LBUTTON :
#         clicked_points.add((y,x))
#         print(y,x)
        
#         for point in clicked_points:
#             image1[segments	== segments[point[0], point[1]]] = color
#         cv2.imshow("image123",image1)
#         clicked_points.clear()
#     elif event == cv2.EVENT_RBUTTONDOWN :
#         cv2.imwrite('C:\\imagestore\\image123ee.jpg', image1)    



# image = cv2.imread('C:\\sample2.jpg')
# clone = image.copy()

# for numSegments in (1000, 5000):

#     segments = slic(image, n_segments = numSegments, sigma = 0.1)

#     fig = plt.figure("Superpixels -- %d segments" % (numSegments))
#     ax = fig.add_subplot(1, 1, 1)

#     color = (255,0,0)
#     image1 = clone.copy()
    
#     cv2.imshow("Aaa",mark_boundaries(image, segments, color=(0.1,0.5,0)))
#     cv2.setMouseCallback("Aaa", MouseLeftClick)

# while True:
#     key = cv2.waitKey(0)
    
#     if key==27:
#         print('key : ',key)
#         break
#     elif key == 113 :
#         color = (100,255,0)
#         print('key : ',key)
# cv2.destroyAllWindows()

